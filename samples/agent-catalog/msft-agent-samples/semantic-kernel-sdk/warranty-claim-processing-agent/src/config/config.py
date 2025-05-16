# This file contains the configuration settings for the Azure AI services and other parameters used in the application.

# Provide your Cognitive Services endpoint
# For example, "https://demo.cognitiveservices.azure.com/"
COGNITIVE_SERVICES_ENDPOINT = ""

# Provide your Azure AI Agent deployment name here for the Risk Assessment Agent
# For example, "demochat"
AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME = ""

# Provide your Azure AI Agent agent ID here for the Risk Assessment Agent
# For example, "asst_jAHzkylLNLt2XgcjKAqa2ozj"
# If empty, the program will create a new agent using the instructions from the file below.
AZURE_AI_AGENT_AGENT_ID = "" 
AGENT_INSTRUCTIONS_PATH = "assets/other/claims_analysis_agent_instructions.md"

INPUT_DOCUMENT_PATH = "assets/input/sample-claim-signed.png" # Path to the claim image document to be processed

# You can mock each agent to return a sample, hardcoded response without calling the AI backend service.
# This allows you to save the cost or reduce latency when debugging the application.
# To mock a respective agent, set the corresponding variable to True.
MOCK_DOC_INTELLIGENCE_STEP = True
MOCK_PII_REDACTION_STEP = True
MOCK_CLAIMS_ANALYSIS_STEP = True