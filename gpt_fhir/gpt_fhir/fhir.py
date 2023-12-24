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

    def __init__(self, config):
        # FHIR client settings
        # fhir_settings = {
        #     "app_id": config["FHIR"]["APP_ID"],
        #     "api_base": config["FHIR"]["API_BASE"],
        # }
        # self.fhir_client = FHIRClient(settings=fhir_settings)
        pass

    def write_condition(self, params):
        """
        This function writes a condition to the FHIR server.
        """
        # Create a new condition object
        new_condition = Condition(self.fhir_client)
        new_condition.code = params["code"]
        new_condition.subject = params["subject"]
        new_condition.onsetDateTime = params["onsetDateTime"]
        new_condition.clinicalStatus = params["clinicalStatus"]
        new_condition.verificationStatus = params["verificationStatus"]
        new_condition.category = params["category"]
        new_condition.severity = params["severity"]
        new_condition.stage = params["stage"]
        new_condition.evidence = params["evidence"]
        new_condition.note = params["note"]
        print(new_condition)

    def write_medication_statement(self, params):
        """
        This function writes a medication statement to the FHIR server.
        """
        # Create a new medication statement object
        new_medication_statement = MedicationStatement(self.fhir_client)
        new_medication_statement.subject = params["subject"]
        new_medication_statement.status = params["status"]
        new_medication_statement.taken = params["taken"]
        new_medication_statement.medicationCodeableConcept = params[
            "medicationCodeableConcept"
        ]
        new_medication_statement.note = params["note"]
        print(new_medication_statement)

    def write_procedure(self, params):
        """
        This function writes a procedure to the FHIR server.
        """
        # Create a new procedure object
        new_procedure = Procedure(self.fhir_client)
        new_procedure.subject = params["subject"]
        new_procedure.status = params["status"]
        new_procedure.code = params["code"]
        new_procedure.performedDateTime = params["performedDateTime"]
        new_procedure.note = params["note"]
        print(new_procedure)
