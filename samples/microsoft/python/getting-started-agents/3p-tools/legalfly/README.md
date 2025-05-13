# LEGALFLY

## Description

Legal insights grounded in trusted sources from your jurisdiction.

## Prerequisites

[Obtain an API key](https://www.legalfly.com/ai-foundry-agents) by filling in the request form. You'll receive the API key by e-mail within 1-2 working days.

## Setup

1. Go to [Azure AI Foundry portal](https://ai.azure.com/) and select your AI Project. Select **Management Center**.

1. Select **+new connection** in the settings page.
1. Select **custom keys** in **other resource types**.

1. Enter the following information to create a connection to store your LEGALFLY key:
   1. Set **Custom keys** to "x-api-key", with the value being your LEGALFLY API key.
   1. Make sure **is secret** is checked.
   1. Set the connection name to your connection name. You use this connection name in your sample code or Foundry Portal later.
   1. For the **Access** setting, you can choose either _this project only_ or _shared to all projects_. Just make sure in your code, the connection string of the project you entered has access to this connection.

## Use LEGALFLY through a code-first experience

1. You can follow the [code sample](./legalfly.py) to use LEGALFLY through Agent SDK.
1. Before running the sample:
   1. pip install azure-ai-agents azure-identity python-dotenv jsonref
   1. Set these environment variables with your own values:
   1. PROJECT_ENDPOINT - the Azure AI Agents connection string.
   1. MODEL - The deployment name of the AI model, as found under the "Name" column in the "Models + endpoints" tab in your Azure AI Foundry project.
   1. LEGALFLY_API_CONNECTION_NAME - The name of the connection for the LegalFly API.

## Customer Support Contact

support@legalfly.com
