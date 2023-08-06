from curses import meta
import json
from ingestion.caris.util.metadata import extract_metadata
from ingestion.caris.util.structural import extract_structural
from ingestion.caris.util.cnv import extract_cnv
from ingestion.caris.util.ga4gh import create_yaml
import os
import pandas as pd

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# Sample status to perform tests without global variables.
INGEST_STATUS = {
    "exome_performed": False,
    "cnv_performed": True,
    "ihc_performed": False,
    "structural_performed": True,
    "run_instructions": {
        "som_vcf": False,
        "germ_vcf": False,
        "som_rna": False,
        "som_structural": False,
        "som_cnv": False,
    },
}


class MockLog:
    def info(self, _: str):
        pass


mock_log = MockLog()


def test_extract_metadata():
    f = open(f"{BASE_PATH}/resources/TN20-779441.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()
    metadata = extract_metadata(
        data, "unit-test", {"pdf": "unit_test.pdf"}, "unit-test.tar.gz", mock_log
    )

    assert metadata == {
        "testType": "MI Profile",
        "indexedDate": "2020-12-08",
        "bodySiteSystem": "http://carislifesciences.com/bodySite",
        "patientIdentifier": "LO-CARIS-1234",
        "patientLastName": "Smith",
        "patientDOB": "1950-10-10",
        "patientFirstName": "Jane",
        "patientGender": "male",
        "diagnosis": "Undifferentiated pleomorphic sarcoma",
        "diagnosisDisplay": "Undifferentiated pleomorphic sarcoma",
        "bodySite": "Ear canal",
        "bodySiteDisplay": "Ear canal",
        "sourceFile": "unit-test.tar.gz",
        "reportFile": ".lifeomic/caris/unit-test/unit_test.pdf",
        "patientInfo": {
            "lastName": "Smith",
            "dob": "1950-10-10",
            "firstName": "Jane",
            "gender": "male",
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": "LO-CARIS-1234",
                }
            ],
        },
        "name": "Caris",
        "reference": "GRCh37",
        "tmb": "high",
        "tmbScore": 33.0,
        "msi": "stable",
        "resources": [{"fileName": ".lifeomic/caris/unit-test/unit_test.pdf"}],
    }


def test_extract_structural():
    f = open(f"{BASE_PATH}/resources/TN20-779441.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()

    metadata = extract_structural("unit-test", data, INGEST_STATUS)

    assert metadata == {
        "fileName": ".lifeomic/caris/unit-test/unit-test.lifted.lifted.structural.csv",
        "sequenceType": "somatic",
        "type": "structuralVariant",
    }

    structural_df = pd.read_csv("unit-test.structural.csv")
    os.remove("unit-test.structural.csv")
    assert structural_df.columns.tolist() == [
        "sample_id",
        "gene1",
        "gene2",
        "effect",
        "chromosome1",
        "start_position1",
        "end_position1",
        "chromosome2",
        "start_position2",
        "end_position2",
        "interpretation",
        "sequence_type",
        "in_frame",
        "attributes",
    ]

    assert structural_df.iloc[0].tolist() == [
        "unit-test",
        "TPM3",
        "ALK",
        "Fusion",
        "chr1",
        154142876,
        154142876,
        "chr2",
        29446394,
        29446394,
        "A TPM3-ALK fusion was detected in this tumor. This fusion has been reported in inflammatory myofibroblastic tumor and anaplastic large cell lymphoma (PMID: 10934142, 10216106). Exon 6 of TPM3 (NM_001278188.1) is joined in-frame to exon 20 of ALK (NM_004304.4)",
        "Somatic",
        "Yes",
        "{}",
    ]
    assert structural_df.iloc[1].tolist() == [
        "unit-test",
        "ST7",
        "MET",
        "Fusion",
        "chr7",
        116739898,
        116739898,
        "chr7",
        116371722,
        116371722,
        "An ST7-MET fusion was detected in this tumor. This fusion is predicted to be in-frame and encode an intact MET kinase domain. It has been reported in glioblastoma (Ferguson 2018 J Neuropathol Exp Neurol 77:437).  Exon 2 of ST7 (NM_021908.2) is joined to exon 3 of MET (NM_001127500.2).",
        "Somatic",
        "Yes",
        "{}",
    ]


def test_extract_cnv():

    data = {
        "tests": [
            {
                "testName": "Exome CNA Panel - Additional Genes",
                "testCode": "CMI1125",
                "platformTechnology": "Exome CNA",
                "testMethodology": "CNA-Seq",
                "testResults": [
                    {
                        "copyNumberAlteration": {
                            "resultCount": "1",
                            "biomarkerName": "ABL1",
                            "gene": "ABL1",
                            "result": "intermediate",
                            "result_group": "No Result",
                            "chromosome": "chr1",
                            "genomicCoordinates": "ABL1:chr1:169076834-169112236",
                            "genomeBuild": "GRCh38/hg38",
                            "genomicSource": "Somatic",
                            "copyNumberType": "intermediate",
                            "copyNumber": "4.10",
                            "dbVarID": "",
                            "interpretation": "",
                            "labSpecific": {
                                "analysisConfigurationName": "NGS5_Exome",
                                "analysisConfigurationVersion": "5.2.5.1",
                                "analysisPipelineName": "NGS",
                                "analysisPipelineVersion": "2.1.3",
                                "NGSPanelName": "Illumina",
                                "NGSPanelVersion": "V12",
                            },
                        }
                    },
                ],
            }
        ]
    }

    metadata = extract_cnv("unit-test", data, INGEST_STATUS)
    f = open("unit-test.copynumber.csv", "r")
    result = f.read().splitlines()
    f.close()
    os.remove("unit-test.copynumber.csv")
    assert result == [
        "sample_id,gene,copy_number,status,attributes,chromosome,start_position,end_position,interpretation",
        "unit-test,ABL1,4.10,gain,{},chr1,169076834,169112236,",
    ]


def test_extract_cnv_del():

    data = {
        "tests": [
            {
                "testName": "Exome CND Panel - Additional Genes",
                "testCode": "CMI1125",
                "platformTechnology": "Exome CNA",
                "testMethodology": "CNA-Seq",
                "testResults": [
                    {
                        "copyNumberAlteration": {
                            "resultCount": "1",
                            "biomarkerName": "ABL1",
                            "gene": "ABL1",
                            "result": "Deleted",
                            "result_group": "Mutated",
                            "genomeBuild": "GRCh38/hg38",
                            "genomicSource": "Somatic",
                            "copyNumberType": "Deleted",
                            "copyNumber": "0.15",
                            "dbVarID": "",
                            "interpretation": "",
                            "labSpecific": {
                                "analysisConfigurationName": "NGS5_Exome",
                                "analysisConfigurationVersion": "5.2.6.3",
                                "analysisPipelineName": "NGS5",
                                "analysisPipelineVersion": "V5.2.8.3",
                                "NGSPanelName": "SureSelect_ExomeV7_plus_720G",
                                "NGSPanelVersion": "V12.0",
                            },
                        }
                    },
                ],
            }
        ]
    }

    metadata = extract_cnv("unit-test", data, INGEST_STATUS)
    f = open("unit-test.copynumber.csv", "r")
    result = f.read().splitlines()
    f.close()
    os.remove("unit-test.copynumber.csv")
    assert result == [
        "sample_id,gene,copy_number,status,attributes,chromosome,start_position,end_position,interpretation",
        "unit-test,ABL1,0.15,loss,{},N/A,,,",
    ]


def test_handle_equivocal():
    f = open(f"{BASE_PATH}/resources/TN20-779441_equivocal.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()
    metadata = extract_metadata(
        data, "unit-test", {"pdf": "unit_test.pdf"}, "unit-test.tar.gz", mock_log
    )

    assert metadata == {
        "testType": "MI Profile",
        "indexedDate": "2020-12-08",
        "bodySiteSystem": "http://carislifesciences.com/bodySite",
        "patientIdentifier": "LO-CARIS-1234",
        "patientLastName": "Smith",
        "patientDOB": "1950-10-10",
        "patientFirstName": "Jane",
        "patientGender": "male",
        "diagnosis": "Undifferentiated pleomorphic sarcoma",
        "diagnosisDisplay": "Undifferentiated pleomorphic sarcoma",
        "bodySite": "Ear canal",
        "bodySiteDisplay": "Ear canal",
        "sourceFile": "unit-test.tar.gz",
        "reportFile": ".lifeomic/caris/unit-test/unit_test.pdf",
        "patientInfo": {
            "lastName": "Smith",
            "dob": "1950-10-10",
            "firstName": "Jane",
            "gender": "male",
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": "LO-CARIS-1234",
                }
            ],
        },
        "name": "Caris",
        "reference": "GRCh37",
        "tmb": "high",
        "tmbScore": 33.0,
        "msi": "indeterminate",
        "resources": [{"fileName": ".lifeomic/caris/unit-test/unit_test.pdf"}],
    }


def test_handle_msi_unknown():
    f = open(f"{BASE_PATH}/resources/TN20-779441_msi_foo.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()
    metadata = extract_metadata(
        data, "unit-test", {"pdf": "unit_test.pdf"}, "unit-test.tar.gz", mock_log
    )

    assert metadata == {
        "testType": "MI Profile",
        "indexedDate": "2020-12-08",
        "bodySiteSystem": "http://carislifesciences.com/bodySite",
        "patientIdentifier": "LO-CARIS-1234",
        "patientLastName": "Smith",
        "patientDOB": "1950-10-10",
        "patientFirstName": "Jane",
        "patientGender": "male",
        "diagnosis": "Undifferentiated pleomorphic sarcoma",
        "diagnosisDisplay": "Undifferentiated pleomorphic sarcoma",
        "bodySite": "Ear canal",
        "bodySiteDisplay": "Ear canal",
        "sourceFile": "unit-test.tar.gz",
        "reportFile": ".lifeomic/caris/unit-test/unit_test.pdf",
        "patientInfo": {
            "lastName": "Smith",
            "dob": "1950-10-10",
            "firstName": "Jane",
            "gender": "male",
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": "LO-CARIS-1234",
                }
            ],
        },
        "name": "Caris",
        "reference": "GRCh37",
        "tmb": "high",
        "tmbScore": 33.0,
        "msi": "foo",
        "resources": [{"fileName": ".lifeomic/caris/unit-test/unit_test.pdf"}],
    }


def test_handle_empty_test():
    f = open(f"{BASE_PATH}/resources/TN20-779441_empty_test.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()
    metadata = extract_metadata(
        data, "unit-test", {"pdf": "unit_test.pdf"}, "unit-test.tar.gz", mock_log
    )

    print(metadata)
    assert metadata == {
        "testType": "MI Profile",
        "indexedDate": "2020-12-08",
        "bodySiteSystem": "http://carislifesciences.com/bodySite",
        "patientIdentifier": "LO-CARIS-1234",
        "patientLastName": "Smith",
        "patientDOB": "1950-10-10",
        "patientFirstName": "Jane",
        "patientGender": "male",
        "diagnosis": "Undifferentiated pleomorphic sarcoma",
        "diagnosisDisplay": "Undifferentiated pleomorphic sarcoma",
        "bodySite": "Ear canal",
        "bodySiteDisplay": "Ear canal",
        "sourceFile": "unit-test.tar.gz",
        "reportFile": ".lifeomic/caris/unit-test/unit_test.pdf",
        "patientInfo": {
            "lastName": "Smith",
            "dob": "1950-10-10",
            "firstName": "Jane",
            "gender": "male",
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": "LO-CARIS-1234",
                }
            ],
        },
        "name": "Caris",
        "reference": "GRCh37",
        "resources": [{"fileName": ".lifeomic/caris/unit-test/unit_test.pdf"}],
    }


def test_equivocal_status():
    f = open(f"{BASE_PATH}/resources/TN20-779441_equivocal_status.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()
    metadata = extract_metadata(
        data, "unit-test", {"pdf": "unit_test.pdf"}, "unit-test.tar.gz", mock_log
    )
    assert metadata == {
        "testType": "MI Profile",
        "indexedDate": "2020-12-08",
        "bodySiteSystem": "http://carislifesciences.com/bodySite",
        "patientIdentifier": "LO-CARIS-1234",
        "patientLastName": "Smith",
        "patientDOB": "1950-10-10",
        "patientFirstName": "Jane",
        "patientGender": "male",
        "diagnosis": "Undifferentiated pleomorphic sarcoma",
        "diagnosisDisplay": "Undifferentiated pleomorphic sarcoma",
        "bodySite": "Ear canal",
        "bodySiteDisplay": "Ear canal",
        "sourceFile": "unit-test.tar.gz",
        "reportFile": ".lifeomic/caris/unit-test/unit_test.pdf",
        "patientInfo": {
            "lastName": "Smith",
            "dob": "1950-10-10",
            "firstName": "Jane",
            "gender": "male",
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": "LO-CARIS-1234",
                }
            ],
        },
        "name": "Caris",
        "reference": "GRCh37",
        "lossOfHeterozygosityScore": 11,
        "lossOfHeterozygosityStatus": "equivocal",
        "resources": [{"fileName": ".lifeomic/caris/unit-test/unit_test.pdf"}],
    }


def test_high_status():
    f = open(f"{BASE_PATH}/resources/TN20-779441_high.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()
    metadata = extract_metadata(
        data, "unit-test", {"pdf": "unit_test.pdf"}, "unit-test.tar.gz", mock_log
    )

    assert metadata == {
        "testType": "MI Profile",
        "indexedDate": "2020-12-08",
        "bodySiteSystem": "http://carislifesciences.com/bodySite",
        "patientIdentifier": "LO-CARIS-1234",
        "patientLastName": "Smith",
        "patientDOB": "1950-10-10",
        "patientFirstName": "Jane",
        "patientGender": "male",
        "diagnosis": "Undifferentiated pleomorphic sarcoma",
        "diagnosisDisplay": "Undifferentiated pleomorphic sarcoma",
        "bodySite": "Ear canal",
        "bodySiteDisplay": "Ear canal",
        "sourceFile": "unit-test.tar.gz",
        "reportFile": ".lifeomic/caris/unit-test/unit_test.pdf",
        "patientInfo": {
            "lastName": "Smith",
            "dob": "1950-10-10",
            "firstName": "Jane",
            "gender": "male",
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": "LO-CARIS-1234",
                }
            ],
        },
        "name": "Caris",
        "reference": "GRCh37",
        "lossOfHeterozygosityScore": 11,
        "lossOfHeterozygosityStatus": "high",
        "resources": [{"fileName": ".lifeomic/caris/unit-test/unit_test.pdf"}],
    }


def test_qns_long_status():
    f = open(f"{BASE_PATH}/resources/TN20-779441_qns_long.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()
    metadata = extract_metadata(
        data, "unit-test", {"pdf": "unit_test.pdf"}, "unit-test.tar.gz", mock_log
    )

    assert metadata == {
        "testType": "MI Profile",
        "indexedDate": "2020-12-08",
        "bodySiteSystem": "http://carislifesciences.com/bodySite",
        "patientIdentifier": "LO-CARIS-1234",
        "patientLastName": "Smith",
        "patientDOB": "1950-10-10",
        "patientFirstName": "Jane",
        "patientGender": "male",
        "diagnosis": "Undifferentiated pleomorphic sarcoma",
        "diagnosisDisplay": "Undifferentiated pleomorphic sarcoma",
        "bodySite": "Ear canal",
        "bodySiteDisplay": "Ear canal",
        "sourceFile": "unit-test.tar.gz",
        "reportFile": ".lifeomic/caris/unit-test/unit_test.pdf",
        "patientInfo": {
            "lastName": "Smith",
            "dob": "1950-10-10",
            "firstName": "Jane",
            "gender": "male",
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": "LO-CARIS-1234",
                }
            ],
        },
        "name": "Caris",
        "reference": "GRCh37",
        "lossOfHeterozygosityScore": 11,
        "lossOfHeterozygosityStatus": "qns",
        "resources": [{"fileName": ".lifeomic/caris/unit-test/unit_test.pdf"}],
    }


def test_qns_status():
    f = open(f"{BASE_PATH}/resources/TN20-779441_qns.json", "rb")
    all_data = json.load(f)
    data = all_data
    f.close()
    metadata = extract_metadata(
        data, "unit-test", {"pdf": "unit_test.pdf"}, "unit-test.tar.gz", mock_log
    )

    assert metadata == {
        "testType": "MI Profile",
        "indexedDate": "2020-12-08",
        "bodySiteSystem": "http://carislifesciences.com/bodySite",
        "patientIdentifier": "LO-CARIS-1234",
        "patientLastName": "Smith",
        "patientDOB": "1950-10-10",
        "patientFirstName": "Jane",
        "patientGender": "male",
        "diagnosis": "Undifferentiated pleomorphic sarcoma",
        "diagnosisDisplay": "Undifferentiated pleomorphic sarcoma",
        "bodySite": "Ear canal",
        "bodySiteDisplay": "Ear canal",
        "sourceFile": "unit-test.tar.gz",
        "reportFile": ".lifeomic/caris/unit-test/unit_test.pdf",
        "patientInfo": {
            "lastName": "Smith",
            "dob": "1950-10-10",
            "firstName": "Jane",
            "gender": "male",
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": "LO-CARIS-1234",
                }
            ],
        },
        "name": "Caris",
        "reference": "GRCh37",
        "lossOfHeterozygosityScore": 11,
        "lossOfHeterozygosityStatus": "qns",
        "resources": [{"fileName": ".lifeomic/caris/unit-test/unit_test.pdf"}],
    }
