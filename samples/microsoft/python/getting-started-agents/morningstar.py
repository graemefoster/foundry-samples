# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use Morningstar data to ground AI agents using the Azure AI Agent Service.

PREREQUISITES:
    1) Create a developer account with Morningstar and obtain your API token.
    2) Set up a custom key connection in the Azure AI Foundry portal with your Morningstar API key.

USAGE:
    python morning_star.py

    Before running the sample:
    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    1) PROJECT_ENDPOINT - the Azure AI Project endpoint.
    2) CONNECTION_ID - the connection ID for the Morningstar custom key connection.
"""

# Import necessary modules
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme

# Set up the project endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]

# Initialize the AIProjectClient to interact with the Azure AI Agents service
project_client = AIProjectClient(
    endpoint=project_endpoint,  # Azure AI Project endpoint
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
    api_version="latest",  # Use the latest API version
)

# Retrieve the connection ID for the Morningstar custom key connection from environment variables
connection_id = os.environ["CONNECTION_ID"]

# Set up authentication details for the Morningstar tool using the connection ID
auth = OpenApiConnectionAuthDetails(
    security_scheme=OpenApiConnectionSecurityScheme(connection_id=connection_id)  # Use the connection ID for authentication
)

# Use the project client within a context manager to ensure proper resource cleanup
with project_client:
    # Create an agent with the Morningstar tool
    agent = project_client.agents.create_agent(
        model="gpt-4o",  # Specify the model to use
        name="MorningstarAgent",  # Name of the agent
        instructions="You are a financial assistant that uses Morningstar data to provide investment insights.",  # Instructions for the agent
        tools=[auth],  # Attach the Morningstar tool to the agent
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Create a user message in the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,  # ID of the thread
        role="user",  # Role of the message sender
        content="What are the top-rated mutual funds according to Morningstar?",  # Message content
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process a run for the agent to handle the message
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Check if the run failed and log the error if applicable
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the agent after the interaction is complete
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"Role: {message['role']}, Content: {message['content']}")
