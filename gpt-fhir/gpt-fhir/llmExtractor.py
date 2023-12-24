from openai import OpenAI


class LLMExtractor:
    """
    This class is responsible for running the FHIR resource extraction using OpenAI's LLM model.
    """

    def __init__(self, config, fhir_tools):
        # copy functions
        self.fhir_tools = fhir_tools

        # set up openai client
        self.client = OpenAI(api_key=config["OPENAI"]["API_KEY"])

    # run a conversation with the model
    def extract(self, text):
        # Step 1: send the conversation and available functions to the model
        messages = [
            {
                "role": "user",
                "content": text,
            }
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=self.fhir_tools.tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            messages.append(
                response_message
            )  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                # function_name = tool_call.function.name
                # function_to_call = available_functions[function_name]
                # function_args = json.loads(tool_call.function.arguments)
                # function_response = function_to_call(
                #    location=function_args.get("location"),
                #    unit=function_args.get("unit"),
                # )
                function_response = self.fhir_tools.run(tool_call)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_call.function.name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )  # get a new response from the model where it can see the function response
            return second_response
