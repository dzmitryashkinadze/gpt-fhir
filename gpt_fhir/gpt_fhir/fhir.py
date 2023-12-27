import logging
from fhirclient.client import FHIRClient

# FHIR types
from fhirclient.models.age import Age
from fhirclient.models.period import Period
from fhirclient.models.dosage import Dosage
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.procedure import Procedure
from fhirclient.models.condition import Condition
from fhirclient.models.annotation import Annotation
from fhirclient.models.condition import ConditionStage
from fhirclient.models.condition import ConditionEvidence
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.medicationstatement import MedicationStatement


class FHIR:
    """
    This class is used to interact with the FHIR server.
    It is used to write the conditions, medication statements and procedures
    that were extracted from doctor's notes to the FHIR server.
    """

    def __init__(self, config, annotator):
        # copy annotator
        self.annotator = annotator

        # FHIR client settings
        fhir_settings = {
            "app_id": config["FHIR"]["APP_ID"],
            "api_base": config["FHIR"]["API_BASE"],
        }
        self.fhir_client = FHIRClient(settings=fhir_settings)

        # init FHIR resources
        self.resources = []

    def empty_resources(self):
        """
        This function empties the resources list.
        """

        self.resources = []

    def get_resources(self):
        """
        This function returns the resources list.
        """

        return self.resources

    def write_condition(self, params):
        """
        This function writes a condition to the FHIR server.
        """

        logging.info(f"FROM LLM: {params}")

        # annotate condition code
        annotations = self.annotator.run(params["condition"])
        if len(annotations) > 0:
            annotation = annotations[0]

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
                        "text": params["condition"],
                    },
                    "subject": {"reference": "Patient/1"},
                    "clinicalStatus": {"text": params["clinicalStatus"]},
                }
            )

            # add abatementAge if present
            if "abatementAge" in params:
                condition.abatementAge = Age({"value": params["abatementAge"]})

            # add abatementDateTime if present
            if "abatementDateTime" in params:
                condition.abatementDateTime = FHIRDate(params["abatementDateTime"])

            # add abatementPeriod if present
            if "abatementPeriod" in params:
                if (
                    type(params["abatementPeriod"]) == dict
                    and "start" in params["abatementPeriod"]
                    and "end" in params["abatementPeriod"]
                ):
                    condition.abatementPeriod = Period(
                        {
                            "start": params["abatementPeriod"]["start"],
                            "end": params["abatementPeriod"]["end"],
                        }
                    )

            # add abatementString if present
            if "abatementString" in params:
                condition.abatementString = params["abatementString"]

            # add bodySite if present
            if "bodySite" in params:
                if type(params["bodySite"]) == list:
                    condition.bodySite = [
                        CodeableConcept({"text": bodySite})
                        for bodySite in params["bodySite"]
                    ]
                else:
                    condition.bodySite = [CodeableConcept({"text": params["bodySite"]})]

            # add category if present
            if "category" in params:
                if type(params["category"]) == list:
                    condition.category = [
                        CodeableConcept({"text": category})
                        for category in params["category"]
                    ]
                else:
                    condition.category = [CodeableConcept({"text": params["category"]})]

            # add evidence if present
            if "evidence" in params:
                if type(params["evidence"]) == list:
                    condition.evidence = [
                        ConditionEvidence({"code": [{"text": evidence}]})
                        for evidence in params["evidence"]
                    ]
                else:
                    condition.evidence = [
                        ConditionEvidence({"code": [{"text": params["evidence"]}]})
                    ]

            # add "note" if present
            if "note" in params:
                if type(params["note"]) == list:
                    condition.note = [
                        Annotation({"text": note}) for note in params["note"]
                    ]
                else:
                    condition.note = [Annotation({"text": params["note"]})]

            # add onsetAge if present
            if "onsetAge" in params:
                condition.onsetAge = Age({"value": params["onsetAge"]})

            # add onsetDateTime if present
            if "onsetDateTime" in params:
                condition.onsetDateTime = FHIRDate(params["onsetDateTime"])

            # add onsetPeriod if present
            if "onsetPeriod" in params:
                if (
                    type(params["onsetPeriod"]) == dict
                    and "start" in params["onsetPeriod"]
                    and "end" in params["onsetPeriod"]
                ):
                    condition.onsetPeriod = Period(
                        {
                            "start": params["onsetPeriod"]["start"],
                            "end": params["onsetPeriod"]["end"],
                        }
                    )

            # add onsetString if present
            if "onsetString" in params:
                condition.onsetString = params["onsetString"]

            # add recordedDate if present
            if "recordedDate" in params:
                condition.recordedDate = FHIRDate(params["recordedDate"])

            # add severity if present
            if "severity" in params:
                condition.severity = CodeableConcept({"text": params["severity"]})

            # add stage if present
            if "stage" in params:
                if type(params["stage"]) == list:
                    condition.stage = [
                        ConditionStage({"summary": {"text": stage}})
                        for stage in params["stage"]
                    ]
                else:
                    condition.stage = [
                        ConditionStage({"summary": {"text": params["stage"]}})
                    ]

            # add verificationStatus if present
            if "verificationStatus" in params:
                condition.verificationStatus = CodeableConcept(
                    {"text": params["verificationStatus"]}
                )

            logging.info(f"FHIR: {condition.as_json()}")

            # add condition to resources list
            self.resources.append(condition.as_json())

            return "Condition was added"

        else:
            return "Condition was not added because code was not found"

    def write_procedure(self, params):
        """
        This function writes a procedure to the FHIR server.
        """

        logging.info(f"FROM LLM: {params}")

        # annotate procedure code
        annotations = self.annotator.run(params["procedure"])
        if len(annotations) > 0:
            annotation = annotations[0]

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
                        "text": params["procedure"],
                    },
                    "status": params["status"],
                    "subject": {"reference": "Patient/1"},
                }
            )

            # add bodySite if present
            if "bodySite" in params:
                if type(params["bodySite"]) == list:
                    procedure.bodySite = [
                        CodeableConcept({"text": bodySite})
                        for bodySite in params["bodySite"]
                    ]
                else:
                    procedure.bodySite = [CodeableConcept({"text": params["bodySite"]})]

            # add category if present
            if "category" in params:
                procedure.category = CodeableConcept({"text": params["category"]})

            # add complication if present
            if "complication" in params:
                if type(params["complication"]) == list:
                    procedure.complication = [
                        CodeableConcept({"text": complication})
                        for complication in params["complication"]
                    ]
                else:
                    procedure.complication = [
                        CodeableConcept({"text": params["complication"]})
                    ]

            # add followUp if present
            if "followUp" in params:
                if type(params["followUp"]) == list:
                    procedure.followUp = [
                        CodeableConcept({"text": followUp})
                        for followUp in params["followUp"]
                    ]
                else:
                    procedure.followUp = [CodeableConcept({"text": params["followUp"]})]

            # add note if present
            if "note" in params:
                if type(params["note"]) == list:
                    procedure.note = [
                        Annotation({"text": note}) for note in params["note"]
                    ]
                else:
                    procedure.note = [Annotation({"text": params["note"]})]

            # add outcome if present
            if "outcome" in params:
                procedure.outcome = CodeableConcept({"text": params["outcome"]})

            # add performedAge if present
            if "performedAge" in params:
                procedure.performedAge = Age({"value": params["performedAge"]})

            # add performedDateTime if present
            if "performedDateTime" in params:
                procedure.performedDateTime = FHIRDate(params["performedDateTime"])

            # add performedPeriod if present
            if "performedPeriod" in params:
                if (
                    type(params["performedPeriod"]) == dict
                    and "start" in params["performedPeriod"]
                    and "end" in params["performedPeriod"]
                ):
                    procedure.performedPeriod = Period(
                        {
                            "start": params["performedPeriod"]["start"],
                            "end": params["performedPeriod"]["end"],
                        }
                    )

            # add performedString if present
            if "performedString" in params:
                procedure.performedString = params["performedString"]

            # add reasonCode if present
            if "reasonCode" in params:
                if type(params["reasonCode"]) == list:
                    procedure.reasonCode = [
                        CodeableConcept({"text": reasonCode})
                        for reasonCode in params["reasonCode"]
                    ]
                else:
                    procedure.reasonCode = [
                        CodeableConcept({"text": params["reasonCode"]})
                    ]

            # add statusReason if present
            if "statusReason" in params:
                procedure.statusReason = CodeableConcept(
                    {"text": params["statusReason"]}
                )

            # add usedCode if present
            if "usedCode" in params:
                if type(params["usedCode"]) == list:
                    procedure.usedCode = [
                        CodeableConcept({"text": usedCode})
                        for usedCode in params["usedCode"]
                    ]
                else:
                    procedure.usedCode = [CodeableConcept({"text": params["usedCode"]})]

            logging.info(f"FHIR: {procedure.as_json()}")

            # add procedure to resources list
            self.resources.append(procedure.as_json())

            return "Procedure was added"

        else:
            return "Procedure was not added because code was not found"

    def write_medication_statement(self, params):
        """
        This function writes a medication statement to the FHIR server.
        """

        logging.info(f"FROM LLM: {params}")

        # annotate medication code
        annotations = self.annotator.run(params["medication_statement"])
        if len(annotations) > 0:
            annotation = annotations[0]

            # create FHIR medication statement
            medication_statement = MedicationStatement(
                {
                    "medicationCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": annotation["obo_id"].split(":")[1],
                                "display": annotation["label"],
                            }
                        ],
                        "text": params["medication_statement"],
                    },
                    "subject": {"reference": "Patient/1"},
                    "status": params["status"],
                }
            )

            # add category if present
            if "category" in params:
                medication_statement.category = CodeableConcept(
                    {"text": params["category"]}
                )

            # add dateAsserted if present
            if "dateAsserted" in params:
                medication_statement.dateAsserted = FHIRDate(params["dateAsserted"])

            # add dosage if present
            if "dosage" in params:
                if type(params["dosage"]) == list:
                    medication_statement.dosage = [
                        Dosage({"text": dosage}) for dosage in params["dosage"]
                    ]
                else:
                    medication_statement.dosage = [Dosage({"text": params["dosage"]})]

            # add effectiveDateTime if present
            if "effectiveDateTime" in params:
                medication_statement.effectiveDateTime = FHIRDate(
                    params["effectiveDateTime"]
                )

            # add effectivePeriod if present
            if "effectivePeriod" in params:
                if (
                    type(params["effectivePeriod"]) == dict
                    and "start" in params["effectivePeriod"]
                    and "end" in params["effectivePeriod"]
                ):
                    medication_statement.effectivePeriod = Period(
                        {
                            "start": params["effectivePeriod"]["start"],
                            "end": params["effectivePeriod"]["end"],
                        }
                    )

            # add note if present
            if "note" in params:
                if type(params["note"]) == list:
                    medication_statement.note = [
                        Annotation({"text": note}) for note in params["note"]
                    ]
                else:
                    medication_statement.note = [Annotation({"text": params["note"]})]

            # add reasonCode if present
            if "reasonCode" in params:
                if type(params["reasonCode"]) == list:
                    medication_statement.reasonCode = [
                        CodeableConcept({"text": reasonCode})
                        for reasonCode in params["reasonCode"]
                    ]
                else:
                    medication_statement.reasonCode = [
                        CodeableConcept({"text": params["reasonCode"]})
                    ]

            # add statusReason if present
            if "statusReason" in params:
                if type(params["statusReason"]) == list:
                    medication_statement.statusReason = [
                        CodeableConcept({"text": statusReason})
                        for statusReason in params["statusReason"]
                    ]
                else:
                    medication_statement.statusReason = [
                        CodeableConcept({"text": params["statusReason"]})
                    ]

            logging.info(f"FHIR: {medication_statement.as_json()}")

            # add medication statement to resources list
            self.resources.append(medication_statement.as_json())

            return "Medication statement was added"

        else:
            return "Medication statement was not added because code was not found"
