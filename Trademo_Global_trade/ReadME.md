# Trademo Shipments and Tariff Tool

This Python script demonstrates how to use Azure AI Projects to create an agent that queries global trade duties using an OpenAPI specification.

## About Tool:
- Name: Trademo_Shipments_And_Tariff
- Description: Provides latest duties and past shipment and duty data for trade between multiple countries


## Features
- Creates an Azure AI Project client
- Sets up OpenAPI connection for global trade data
- Processes trade duty queries
- Handles thread/message management

## Prerequisites
- Azure subscription
- Azure AI Projects resource
- Python 3.8+
- Azure CLI installed and logged in
- Required Python packages:
  - azure-ai-projects
  - azure-identity
  - jsonref

## Installation
Install dependencies:
```bash
pip install azure-ai-projects azure-identity jsonref
```


## Usage
Run the script:
```bash
python global_trade.py
```

Before running the sample:

Obtain the sessionid from trademo which serves as the API_KEY.

Set up a custom key connection, name the key as 'sessionid' and save the connection name.

Save that connection name as the PROJECT_OPENAPI_CONNECTION_NAME environment variable


Set this environment variables with your own values:
PROJECT_CONNECTION_STRING - the Azure AI Project connection string, as found in your Foundry Project.
PROJECT_OPENAPI_CONNECTION_NAME - the connection name for the OpenAPI connection authentication
MODEL_DEPLOYMENT_NAME - name of the model deployment in the project to use Agents against

## Example queries processed by the tool:
- "How many GPUs(HS code 847330) were imported to United States from China in February 2025?"
- "which were the top countries based on shipment value that exported jewellery(HS code 711319) to usa in 2024?"
- "Which countries are the biggest exporter of lithium ion battery(HS code 850760) to the US in 2024?"
- "what is the duty of import for jewllery(HS code =  711319) from India to US?"
- "Compare current duties on lithium ion batteries(HS code 850760) imported to US"

## Notes
- The script creates and deletes the agent during execution
- OpenAPI connection requires additional setup in Azure
- The agent assumes HS 6-digit codes for products automatically
- Error handling is included for failed runs


## Contact
For any queries, please follow the below escalation matrix:
- [support@trademo.com](mailto:support@trademo.com)
- [akshit.gupta@trademo.com](mailto:akshit.gupta@trademo.com)
- [devesh@trademo.com](mailto:devesh@trademo.com)