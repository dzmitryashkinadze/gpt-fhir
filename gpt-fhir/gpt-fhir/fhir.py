from fhirclient.models.observation import Observation
from fhirclient.models.condition import Condition
from fhirclient.models.medicationstatement import MedicationStatement
from fhirclient.models.medication import Medication
from fhirclient.models.procedure import Procedure
from fhirclient.models.annotation import Annotation
from fhirclient.models.patient import Patient
from fhirclient.client import FHIRClient


class FHIR:
    """
    This class is used to interact with the FHIR server.
    It is used to write the conditions, medication statements and procedures
    that were extracted from doctor's notes to the FHIR server.
    """

    def __init__(self, config):
        # FHIR client settings
        fhir_settings = {
            "app_id": config["FHIR"]["app_id"],
            "api_base": config["FHIR"]["api_base"],
        }
        self.fhir_client = FHIRClient(settings=fhir_settings)

    def write_condition(self, condition):
        """
        This function writes a condition to the FHIR server.
        """
        # Create a new condition object
        new_condition = Condition(self.fhir_client)
        new_condition.code = condition["code"]
        new_condition.subject = condition["subject"]
        new_condition.onsetDateTime = condition["onsetDateTime"]
        new_condition.clinicalStatus = condition["clinicalStatus"]
        new_condition.verificationStatus = condition["verificationStatus"]
        new_condition.category = condition["category"]
        new_condition.severity = condition["severity"]
        new_condition.stage = condition["stage"]
        new_condition.evidence = condition["evidence"]
        new_condition.note = condition["note"]
        new_condition.save()

    def write_medication_statement(self, medication_statement):
        """
        This function writes a medication statement to the FHIR server.
        """
        # Create a new medication statement object
        new_medication_statement = MedicationStatement(self.fhir_client)
        new_medication_statement.subject = medication_statement["subject"]
        new_medication_statement.status = medication_statement["status"]
        new_medication_statement.medicationCodeableConcept = medication_statement[
            "medicationCodeableConcept"
        ]
        new_medication_statement.dosage = medication_statement["dosage"]
        new_medication_statement.save()

    def write_procedure(self, procedure):
        """
        This function writes a procedure to the FHIR server.
        """
        # Create a new procedure object
        new_procedure = Procedure(self.fhir_client)
        new_procedure.subject = procedure["subject"]
        new_procedure.status = procedure["status"]
        new_procedure.code = procedure["code"]
        new_procedure.performedDateTime = procedure["performedDateTime"]
        new_procedure.save()
