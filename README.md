# GenAI driven NLP annotation of FHIR notes
A sizeable portion of all medical records are not structured at all. For example, doctor's notes, often rich in context and critical patient insights, primarily exist in unstructured formats (typed or even recorded notes).
Extraction of structured FHIR resources such as patient health conditions, medical procedures, taken or prescribed medications, and many others from such unstructured data is not trivial as it covers a huge universe of possible patient health conditions and their written descriptions.
Here I showcase how to extract FHIR resources from free text using function calling from OpenAI LLM models.

## Requirements
* Access to OpenAI API
* Python 3.11 (I use conda)

## Set up
* Create a new conda environment
  ```
  conda create --name gprfhir python=3.11
  ```
* Activate it.
  ```
  conda activate gprfhir
  ```
* Install dependencies
  ```
  python -m pip install -r requirements.txt
  ```
* Install main package
  ```
  cd gpt_fhir
  python -m pip install -e .
  ```
* Configure your OpenAI API access (for this change **API_KEY** in *config.yaml.example* and rename it to *config.yaml*)

## Test it
To get an initial feel about the package you can either have a look in *notebooks/gptfhir.ipynb* or execute a test script
```
from gpt_fhir.llmExtractor import LLMExtractor
from gpt_fhir.fhirTools import FHIRTools
from gpt_fhir.fhir import FHIR
from gpt_fhir.annotator import Annotator

# load the config file
with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

# set up annotator
annotator = Annotator()

# set up FHIR client
fhir = FHIR(annotator)

# set up FHIR tools
fhir_tools = FHIRTools(config, fhir)

# set up llm chat
llm_extractor = LLMExtractor(config, fhir_tools)

# test llm extractor
text = "patient has a history of diabetes"
llm_extractor.extract(text)

# print extracted FHIR resources
print(fhir.get_resources())
```
