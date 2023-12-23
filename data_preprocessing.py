import pandas as pd
from ols_client import EBIClient
from fhirclient.models.condition import Condition
from fhirclient.models.medicationstatement import MedicationStatement
from fhirclient.models.procedure import Procedure

# import data
diagnosis = pd.read_csv("../data/diagnosis_notes.csv")
medication = pd.read_csv("../data/medication_notes.csv")
procedure = pd.read_csv("../data/procedure_notes.csv")

# set up EBI client
ebi_client = EBIClient()


# get SNOMED annotations for term
def get_annorations(text):
    return ebi_client.search(query=text, params={"ontology": "snomed"})


# create FHIR JSON from diagnosis
def create_condition(d, annotation):
    # create FHIR condition
    condition = Condition(
        {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": annotation["obo_id"].split(":")[1],
                        "display": annotation["label"],
                    }
                ],
                "text": d["diagnosis"],
            },
            "subject": {"reference": "Patient/1"},
            "clinicalStatus": {"text": "active"},
        }
    )

    return condition.as_json()


# create FHIR JSON from medication
def create_medication(d, annotation):
    # create FHIR medication
    medication = MedicationStatement(
        {
            "medicationCodeableConcept": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": annotation["obo_id"].split(":")[1],
                        "display": annotation["label"],
                    }
                ],
                "text": d["medication"],
            },
            "subject": {"reference": "Patient/1"},
            "status": "recorded",
        }
    )

    return medication.as_json()


# create FHIR JSON from procedure
def create_procedure(d, annotation):
    # create FHIR procedure
    procedure = Procedure(
        {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": annotation["obo_id"].split(":")[1],
                        "display": annotation["label"],
                    }
                ],
                "text": d["procedure"],
            },
            "subject": {"reference": "Patient/1"},
            "status": "completed",
        }
    )

    return procedure.as_json()


# process each row
def process_condition_row(d):
    # get first annotation
    annotation = get_annorations(d["diagnosis"])[0]

    # return the created condition
    return create_condition(d, annotation)


# process each row
def process_medication_row(d):
    # get first annotation
    annotation = get_annorations(d["medication"])[0]

    # return the created medication
    return create_medication(d, annotation)


# process each row
def process_procedure_row(d):
    # get first annotation
    annotation = get_annorations(d["procedure"])[0]

    # return the created procedure
    return create_procedure(d, annotation)


# apply the function to each row
diagnosis["fhir"] = diagnosis.apply(process_condition_row, axis=1)
medication["fhir"] = medication.apply(process_medication_row, axis=1)
procedure["fhir"] = procedure.apply(process_procedure_row, axis=1)

# combine all 3 dataframes by taking only note and fhir columns
combined = pd.concat(
    [
        diagnosis[["note", "fhir"]],
        medication[["note", "fhir"]],
        procedure[["note", "fhir"]],
    ]
)

# write to file
combined.to_csv("../data/fhir_notes.csv", index=False)
