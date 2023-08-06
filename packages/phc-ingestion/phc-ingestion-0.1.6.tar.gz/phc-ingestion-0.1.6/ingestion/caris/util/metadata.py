import pandas as pd
from logging import Logger

MSI_MAPPINGS = {
    "low": "low",
    "stable": "stable",
    "high": "high",
    "indeterminate": "indeterminate",
    "equivocal": "indeterminate",
}

# Build up the manifest iteratively because almost everything is optional
def extract_metadata(data, prefix, files, infile, log: Logger):
    metadata = {}

    test_details = data["testDetails"]

    metadata["testType"] = "MI Profile"

    #  Get the date without the time
    metadata["indexedDate"] = test_details["receivedDate"].split()[0]

    patient = data["patientInformation"]
    metadata["bodySiteSystem"] = "http://carislifesciences.com/bodySite"
    metadata["patientIdentifier"] = patient["mrn"]
    metadata["patientLastName"] = patient["lastName"]

    metadata["patientDOB"] = patient["dob"]
    metadata["patientFirstName"] = patient["firstName"]

    metadata["patientGender"] = patient["gender"].lower()
    metadata["diagnosis"] = patient["diagnosis"]
    metadata["diagnosisDisplay"] = metadata["diagnosis"]

    metadata["bodySite"] = data["specimenInformation"]["tumorSpecimenInformation"]["specimenSite"]
    metadata["bodySiteDisplay"] = metadata["bodySite"]
    metadata["sourceFile"] = infile
    pdf = files["pdf"]
    metadata["reportFile"] = f".lifeomic/caris/{prefix}/{pdf}"

    # Some patients do not have an MRN
    patientInfo = (
        {
            "lastName": metadata["patientLastName"],
            "dob": metadata["patientDOB"],
            "firstName": metadata["patientFirstName"],
            "gender": metadata["patientGender"],
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": metadata["patientIdentifier"],
                }
            ],
        }
        if metadata["patientIdentifier"]
        else {
            "lastName": metadata["patientLastName"],
            "dob": metadata["patientDOB"],
            "firstName": metadata["patientFirstName"],
            "gender": metadata["patientGender"],
        }
    )

    # Ensure no null entries
    metadata["patientInfo"] = {k: v for k, v in patientInfo.items() if v}
    metadata.update({"name": "Caris", "reference": "GRCh37"})

    # Now find the test information

    tests = data["tests"]

    msi = None
    tmb = None
    tmbScore = None
    ihc_run_count = 0
    tmbUnit = None
    global EXOME_PERFORMED
    global CNV_PERFORMED
    global STRUCTURAL_PERFORMED
    global IHC_PERFORMED

    i = 0
    # if not sufficient quantity we won't have test results
    if test_details["reportType"] != "QNS":
        for test in tests:
            if (
                "clinical genes" in test["testName"].lower()
                and "test_cancellation_reason" not in test.keys()
                and test["testMethodology"] == "Seq"
            ):
                # They don't always do exome sequencing
                EXOME_PERFORMED = True
                for info in test["testResults"]:
                    if "tumorMutationBurden" in info.keys():
                        tmb = info["tumorMutationBurden"]["mutationBurdenCall"].lower()
                        tmbScore = info["tumorMutationBurden"]["mutationBurdenScore"]
                        if not tmbScore:
                            continue
                        tmbUnit = info["tumorMutationBurden"]["mutationBurdenUnit"]
                        # Convert from their format, which is "21 per Mb"
                        if tmbUnit == "Mutations/Megabase":
                            tmbScore = float(tmbScore.split(" per")[0])
                        metadata["tmb"] = tmb
                        metadata["tmbScore"] = tmbScore
                    elif "microsatelliteInstability" in info.keys():
                        # if the key isn't found we will get an error during manifest processing
                        # it would be better to fail here, i.e. fail fast, but our alerting
                        # is much better at the manifest level so doing a default value for now
                        msi_key = info["microsatelliteInstability"]["msiCall"].lower()
                        if msi_key in MSI_MAPPINGS:
                            metadata["msi"] = MSI_MAPPINGS[msi_key]
                        else:
                            metadata["msi"] = msi_key
                    elif "genomicLevelHeterozygosity" in info.keys():
                        loh_status = info["genomicLevelHeterozygosity"]["result"].lower()
                        loh_score = info["genomicLevelHeterozygosity"]["LOHpercentage"]
                        # This comes out as a string, convert to integer for proper ingestion
                        metadata["lossOfHeterozygosityScore"] = int(loh_score)
                        metadata["lossOfHeterozygosityStatus"] = (
                            "qns" if loh_status == "quality not sufficient" else loh_status
                        )
            elif (
                "CNA" in test["testName"] or "CND" in test["testName"]
            ) and "test_cancellation_reason" not in test.keys():
                CNV_PERFORMED = True
                log.info(f"Copy Number Alteration testing identified: {test['testName']} ")
            elif (
                "Transcriptome" in test["testName"]
                and "test_cancellation_reason" not in test.keys()
            ):
                STRUCTURAL_PERFORMED = True
                log.info(f"Structural Variant testing identified: {test['testName']}")
            # elif ("PD-L1" in test['testName'] or "Mismatch Repair Status" in test['testName']) and 'test_cancellation_reason' not in test.keys():
            elif "IHC" in test["testMethodology"] and "test_cancellation_reason" not in test.keys():
                IHC_PERFORMED = True
                ihc_run_count += 1
                #  if ihc_run_count <=1:
                #      metadata['ihc']= immunohistochemistry(prefix, data)
                log.info(f"IHC testing identified: {test['testName']}")
            i += 1
    # Add in the additional resources as linkable
    metadata["resources"] = []
    ingest_files = [
        "nrm.vcf.gz",
        "tmp",
        "ga4gh.tmp",
        "runner",
        "yml",
        "ga4gh.yml",
        "copynumber.csv",
        "structural.csv",
    ]
    for ext, filename in files.items():
        if ext not in ingest_files:
            if ext != "bam" and "fastq" not in ext:
                metadata["resources"].append({"fileName": f".lifeomic/caris/{prefix}/{filename}"})
            else:
                for f in files[ext]:
                    metadata["resources"].append({"fileName": f".lifeomic/caris/{prefix}/{f}"})
                    if ext == "bam":
                        metadata["resources"].append(
                            {"fileName": f".lifeomic/caris/{prefix}/{f}.bai"}
                        )
            # If we got RNAseq results let us also make json files available
            if ext == "tsv":
                metadata["resources"].append(
                    {"fileName": f".lifeomic/caris/{prefix}/{prefix}.expression.cancerscope.json"}
                )
                metadata["resources"].append(
                    {"fileName": f".lifeomic/caris/{prefix}/{prefix}.expression.pcann.json"}
                )

    active_metadata = {k: v for k, v in metadata.items() if v is not None}
    return active_metadata


# This will have to be re-written now that we are handling all IHC
def immunohistochemistry(prefix, data):
    tests = []
    ihc_results = []
    for test in data["tests"]:
        #    if "PD-L1" in test['testName'] or "Mismatch Repair Status" in test['testName']:
        if test["testMethodology"] == "IHC" and "test_cancellation_reason" not in test.keys():
            for test_result in test["testResults"]:
                this_result = test["testResults"][test_result]
                # Some steps have "tc" prefixed results.... especially a certain PD-L1 test
                # This means they tested both tumor cells and IC and will process both.
                if (
                    "tcResult" in this_result.keys()
                    and "icResult" in this_result.keys()
                    and "icStainPercent" in this_result.keys()
                ):

                    tc = {}
                    tc["stainPercent"] = this_result["tcStainPercent"]
                    tc["intensity"] = this_result["tcIntensity"]
                    tc["result"] = this_result["tcResult"]
                    tc["biomarkerName"] = this_result[
                        "biomarkerName"
                    ]  # f'{this_result["biomarkerName"]} - TC'

                    tests.append(tc)
                    # THIS IS UNTIL WE FIGURE OUT HOW WE WANT TO INGEST THIS SPECIFIC TEST
                    continue
                # this_result['stainPercent'] = this_result['icStainPercent']
                # this_result['intensity'] = ''
                # this_result['result'] = this_result['icResult']
                # this_result['biomarkerName'] = #f'{this_result["biomarkerName"]} - IC'

                # In this case we only have the tumor cell information
                elif "tcResult" in this_result.keys():
                    this_result["stainPercent"] = this_result["tcStainPercent"]
                    this_result["intensity"] = this_result["tcIntensity"]
                    this_result["result"] = this_result["tcResult"]
                    this_result["biomarkerName"] = this_result[
                        "biomarkerName"
                    ]  # f'{this_result["biomarkerName"]} - TC'

                tests.append(this_result)

    df = pd.DataFrame(tests)
    df = df.to_dict("records")
    for item in df:
        intensity = item["intensity"]
        stainpercent = (
            item["stainPercent"] if not item["stainPercent"] else int(item["stainPercent"])
        )
        biomarkername = item["biomarkerName"]
        result = item["result"]
        # We didn't get a full result list but here's what I could come up with from the test data...
        if result not in ["Technical Issues", "Negative", "Other", "Indeterminate"]:
            if biomarkername == "Mismatch Repair Status":
                ihc_results.append({"biomarkerName": biomarkername, "result": result})
            elif biomarkername == "PD-L1 IC(SP142) - IC":
                ihc_results.append(
                    {"biomarkerName": biomarkername, "result": result, "stainPercent": stainpercent}
                )
            else:
                ihc_results.append(
                    {
                        "biomarkerName": biomarkername,
                        "result": result,
                        "intensity": intensity,
                        "stainPercent": stainpercent,
                    }
                )

    return ihc_results
