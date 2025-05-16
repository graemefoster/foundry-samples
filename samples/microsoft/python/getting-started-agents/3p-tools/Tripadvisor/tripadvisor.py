# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use Tripadvisor from
    the Azure AI Agent service using a synchronous client.

USAGE:
    python tripadvisor.py

    Before running the sample:

    pip install azure-ai-projects azure-ai-agents azure-identity

    Set these environment variables with your own values:
    1) PROJECT_ENDPOINT - the Azure AI Agent endpoint.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
"""

# <create a project client>
import os
import jsonref
from azure.identity import DefaultAzureCredential
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import MessageRole, OpenApiTool, OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme


# Format of the project_endpoint is https://<your-ai-services-account-name>.services.ai.azure.com/api/projects/<your-project-name>
project_endpoint = "YOUR_ENDPOINT"
# Change if you deployed a different model
model_deployment_name = "gpt-4o"

# 1RP update: create a project client in the following way
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

with project_client:
    agents_client = project_client.agents.get_client()
  
    # Upload OpenAPI spec and wait for it to be processed
    # [START create_agent_with_openapi]
    # Update the file path to the correct location
    with open('./tripadvisor.json', 'r', encoding='utf-8') as f:
        openapi_spec = jsonref.loads(f.read())  # Update this to your file path

    # Create Auth object for the OpenApiTool (note that connection or managed identity auth setup requires additional setup in Azure)
    # Your connection id should be in this format if you created under project scope: /subscriptions/SUBSCRIPTION_ID/resourceGroups/RESOURCE_GROUP_NAME/providers/Microsoft.CognitiveServices/accounts/AI_SERVICE_NAME/projects/PROJECT_NAME/connections/CONNECTION_NAME
    auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id="YOUR_CONNECTION_ID"))

    # Initialize agent OpenApi tool using the read in OpenAPI spec
    openapi = OpenApiTool(name="tripadvisor", spec=openapi_spec, description="get reviews for restaurants and hotels given locations", auth=auth)
    
    # Create agent th openapi spec tool
    agent = agents_client.create_agent(
        model=model_deployment_name,
        name="my-agent",
        instructions="You are helpful agent",
        tools=openapi.definitions,
    )
    # [END create_agent_with_openapi]
    print(f"Created agent, agent ID: {agent.id}")

    thread = agents_client.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Create a message
    message = agents_client.create_message(
        thread_id=thread.id,
        role="user",
        content="top 5 hotels in paris and their review links",
    )
    print(f"Created message, message ID: {message.id}")

    run = agents_client.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # Delete the agent when done
    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages
    messages = agents_client.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")
