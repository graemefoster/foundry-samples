# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
FILE: tripadvisor_sample_code.py

DESCRIPTION:
    This sample demonstrates how to use agent operations with the 
    OpenAPI tool from the Azure Agents service using a synchronous client, using
    customKeys authentication against the Tripadvisor API.
    To learn more about OpenAPI specs, visit https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/openapi-spec

USAGE:
    python tripadvisor_sample_code.py

    Before running the sample:

    Set up an account at https://www.tripadvisor.com/developers and get an API key.

    Set up a customKeys connection and save the connection name following the steps at
    https://aka.ms/azsdk/azure-ai-agents/custom-key-setup

    pip install azure-ai-agents azure-identity jsonref

    Set this environment variables with your own values:
    PROJECT_ENDPOINT - the Azure AI Agents endpoint.
    CONNECTION_ID - the connection ID for the customKeys connection, taken from Azure AI Foundry.
    MODEL_DEPLOYMENT_NAME - name of the model deployment in the project to use Agents against
"""

import os
import jsonref
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import OpenApiTool, OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme


agents_client = AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

model_name = os.environ["MODEL_DEPLOYMENT_NAME"]
# connection_id should be in the format of "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{AIservicename}/projects/{projectName}/connections/{connectionName}"
connection_id = os.environ["CONNECTION_ID"]

with open("./tripadvisor.json", "r") as f:
    openapi_spec = jsonref.loads(f.read())

# Create Auth object for the OpenApiTool (note that connection or managed identity auth setup requires additional setup in Azure)
auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id=connection_id))

# Initialize an Agent OpenApi tool using the read in OpenAPI spec
openapi = OpenApiTool(
    name="tripadvisor", 
    spec=openapi_spec, 
    description="get travel data, guidance, and reviews", 
    auth=auth
)

# Create an Agent with OpenApi tool and process Agent run
with agents_client:
    agent = agents_client.create_agent(
        model=model_name, 
        name="my-travel-planning-agent", 
        instructions="You are a helpful travel planning agent. Use the tool to retrieve travel data given a specific location.", 
        tools=openapi.definitions
    )
    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = agents_client.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Create message to thread
    message = agents_client.messages.create(
        thread_id=thread.id, 
        role="user", 
        content="top 5 hotels in Paris and their review links")
    print(f"Created message: {message['id']}")

    # Create and process an Agent run in thread with tools
    run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the Agent when done
    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages
    messages = agents_client.messages.list(thread_id=thread.id)
    print(f"Messages: {messages}")