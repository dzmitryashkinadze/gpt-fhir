class FHIRTools:
    """
    This class contains the functions that can be called by the LLM model.
    Each function with description creates a FHIR resource
    """

    def __init__(self, config, fhir):
        # define tools from config
        self.tools = config["GENAI"]["TOOLS"]

        # copy over the fhir client
        self.fhir = fhir

    def extract_fhir_condition(self, params):
        """Extract a FHIR condition"""
        return self.fhir.create_condition(params)

    def extract_fhir_medication_statement(self, params):
        """Extract a FHIR medication statement"""
        return self.fhir.create_medication_statement(params)

    def extract_fhir_procedure(self, params):
        """Extract a FHIR procedure"""
        return self.fhir.create_procedure(params)

    def run(self, tool_call):
        """Run a tool"""

        # extract tool name and params
        tool_name = tool_call["tool"]
        tool_parameters = tool_call["parameters"]

        # run tool
        match tool_name:
            case "extract_fhir_condition":
                return self.extract_fhir_condition(tool_parameters)
            case "extract_fhir_medication_statement":
                return self.extract_fhir_medication_statement(tool_parameters)
            case "extract_fhir_procedure":
                return self.extract_fhir_procedure(tool_parameters)
