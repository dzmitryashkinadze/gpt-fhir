import json


class FHIRTools:
    """
    This class contains the functions that can be called by the LLM model.
    Each function with description creates a FHIR resource
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    # Example dummy function hard coded to return the same weather
    # In production, this could be your backend API or an external API
    def get_current_weather(self, location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        if "tokyo" in location.lower():
            return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
        elif "san francisco" in location.lower():
            return json.dumps(
                {"location": "San Francisco", "temperature": "72", "unit": unit}
            )
        elif "paris" in location.lower():
            return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
        else:
            return json.dumps({"location": location, "temperature": "unknown"})

    def run(self, tool_call):
        # Step 1: get the tool call
        tool_name = tool_call["tool"]
        tool_parameters = tool_call["parameters"]
        # Step 2: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": self.get_current_weather,
            "get_patient": self.get_patient,
            "get_condition": self.get_condition,
            "get_medication": self.get_medication,
            "get_medication_statement": self.get_medication_statement,
            "get_procedure": self.get_procedure,
            "get_observation": self.get_observation,
            "get_annotation": self.get_annotation,
        }
        return None
