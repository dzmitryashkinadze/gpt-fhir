import json


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

    def run(self, tool_call):
        """Run a tool"""

        # extract tool name and params
        tool_name = tool_call.function.name
        tool_parameters = json.loads(tool_call.function.arguments)

        # run tool
        match tool_name:
            case "extract_fhir_condition":
                return self.fhir.write_condition(tool_parameters)
            case "extract_fhir_medication_statement":
                return self.fhir.write_medication_statement(tool_parameters)
            case "extract_fhir_procedure":
                return self.fhir.write_procedure(tool_parameters)
