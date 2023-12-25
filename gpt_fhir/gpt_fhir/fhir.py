from fhirclient.models.condition import Condition
from fhirclient.models.medicationstatement import MedicationStatement
from fhirclient.models.procedure import Procedure
from fhirclient.client import FHIRClient


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

    def write_condition(self, params):
        """
        This function writes a condition to the FHIR server.
        """

        # serialize params
        print(params)

        # annotate condition code
        annotations = self.annotator.run(params["code"])
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
                        "text": params["code"],
                    },
                    "subject": {"reference": "Patient/1"},
                    "clinicalStatus": {"text": params["clinicalStatus"]},
                }
            )

            # add verificationStatus if present
            if "verificationStatus" in params:
                condition.verificationStatus = {"text": params["verificationStatus"]}

            # add category if present
            if "category" in params:
                condition.category = params["category"]

            # add severity if present
            if "severity" in params:
                condition.severity = params["severity"]

            # add bodySite if present
            if "bodySite" in params:
                condition.bodySite = params["bodySite"]

            # add onsetDateTime if present
            if "onsetDateTime" in params:
                condition.onsetDateTime = params["onsetDateTime"]

            # add onsetAge if present
            if "onsetAge" in params:
                condition.onsetAge = params["onsetAge"]

            # add onsetString if present
            if "onsetString" in params:
                condition.onsetString = params["onsetString"]

            # add abatementDateTime if present
            if "abatementDateTime" in params:
                condition.abatementDateTime = params["abatementDateTime"]

            # add abatementAge if present
            if "abatementAge" in params:
                condition.abatementAge = params["abatementAge"]

            # add abatementString if present
            if "abatementString" in params:
                condition.abatementString = params["abatementString"]

            # add recordedDate if present
            if "recordedDate" in params:
                condition.recordedDate = params["recordedDate"]

            # add stage if present
            if "stage" in params:
                condition.stage = params["stage"]

            # add evidence if present
            if "evidence" in params:
                condition.evidence = params["evidence"]

            # add "note" if present
            if "note" in params:
                condition.note = params["note"]

            print(condition.as_json())

            return "Condition was added"

        else:
            return "Condition was not added"

    def write_medication_statement(self, params):
        """
        This function writes a medication statement to the FHIR server.
        """

        # serialize params
        print(params)

        # annotate medication code
        annotations = self.annotator.run(params["medicationCodeableConcept"])
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
                        "text": params["medicationCodeableConcept"],
                    },
                    "subject": {"reference": "Patient/1"},
                    "status": params["status"],
                }
            )

            # add effectiveDateTime if present
            if "effectiveDateTime" in params:
                medication_statement.effectiveDateTime = params["effectiveDateTime"]

            # add effectivePeriod if present
            if "effectivePeriod" in params:
                medication_statement.effectivePeriod = params["effectivePeriod"]

            # add dateAsserted if present
            if "dateAsserted" in params:
                medication_statement.dateAsserted = params["dateAsserted"]

            # add informationSource if present
            if "informationSource" in params:
                medication_statement.informationSource = params["informationSource"]

            # add derivedFrom if present
            if "derivedFrom" in params:
                medication_statement.derivedFrom = params["derivedFrom"]

            # add reasonCode if present
            if "reasonCode" in params:
                medication_statement.reasonCode = params["reasonCode"]

            # add reasonReference if present
            if "reasonReference" in params:
                medication_statement.reasonReference = params["reasonReference"]

            # add note if present
            if "note" in params:
                medication_statement.note = params["note"]

            print(medication_statement.as_json())

            return "Condition was added"

        else:
            return "Condition was not added"

    def write_procedure(self, params):
        """
        This function writes a procedure to the FHIR server.
        """

        # serialize params
        print(params)

        # annotate procedure code
        annotations = self.annotator.run(params["code"])
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
                        "text": params["code"],
                    },
                    "subject": {"reference": "Patient/1"},
                }
            )

            # add performedDateTime if present
            if "performedDateTime" in params:
                procedure.performedDateTime = params["performedDateTime"]

            # add performedPeriod if present
            if "performedPeriod" in params:
                procedure.performedPeriod = params["performedPeriod"]

            # add performedString if present
            if "performedString" in params:
                procedure.performedString = params["performedString"]

            # add performedAge if present
            if "performedAge" in params:
                procedure.performedAge = params["performedAge"]

            # add performedRange if present
            if "performedRange" in params:
                procedure.performedRange = params["performedRange"]

            # add recorder if present
            if "recorder" in params:
                procedure.recorder = params["recorder"]

            # add asserter if present
            if "asserter" in params:
                procedure.asserter = params["asserter"]

            # add performer if present
            if "performer" in params:
                procedure.performer = params["performer"]

            # add location if present
            if "location" in params:
                procedure.location = params["location"]

            # add outcome if present
            if "outcome" in params:
                procedure.outcome = params["outcome"]

            # add report if present
            if "report" in params:
                procedure.report = params["report"]

            # add complication if present
            if "complication" in params:
                procedure.complication = params["complication"]

            # add complicationDetail if present
            if "complicationDetail" in params:
                procedure.complicationDetail = params["complicationDetail"]

            # add followUp if present
            if "followUp" in params:
                procedure.followUp = params["followUp"]

            # add note if present
            if "note" in params:
                procedure.note = params["note"]

            print(procedure.as_json())

            return "Condition was added"

        else:
            return "Condition was not added"
