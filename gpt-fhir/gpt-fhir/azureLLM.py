from langchain.llms import AzureOpenAI
import os
import openai

class AzureLLM:
    """ 
    Collection of 2 LangChain wrappers of
    Accenture's Azure LLM (gpt-4) and 
    Embeding (ext-embedding-ada-002) model deployments
    """

    def __init__(self, config):

        openai.api_type = config['AZURE']['AZURE_API_TYPE']
        openai.api_base = config['AZURE']['AZURE_API_BASE']
        openai.api_version = config['AZURE']['AZURE_API_VERSION']
        openai.api_key = config['AZURE']['AZURE_API_KEY']

        # llm model
        self.llm = AzureOpenAI(
            model_name=config['AZURE']['AZURE_LLM_DEPLOYMENT'],
            engine=config['AZURE']['AZURE_LLM_DEPLOYMENT'],
        )