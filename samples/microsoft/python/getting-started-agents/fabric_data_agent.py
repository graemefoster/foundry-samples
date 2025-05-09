# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
FILE: fabric_data_agent.py

DESCRIPTION:
    This sample demonstrates how to use agent operations with the Fabric tool from
    the Azure Agents service using a synchronous client.

USAGE:
    python fabric_data_agent.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    PROJECT_ENDPOINT - The Azure AI Project endpoint, as found in your AI Studio Project.
    MODEL_DEPLOYMENT_NAME - The deployment name of the AI model.
    FABRIC_CONNECTION_ID - The connection ID for the Fabric tool.
"""

import os
from azure.identity import DefaultAzureCredential  # For authentication
from azure.ai.projects import AIProjectClient  # Client to interact with Azure AI Projects
from azure.ai.agents.models import FabricTool  # Tool for interacting with Fabric resources

# Define the path to the asset file (replace with your actual file path)
asset_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/product_info_1.md"))

# Retrieve the endpoint, model deployment name, and Fabric connection ID from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # Ensure the MODEL_DEPLOYMENT_NAME environment variable is set
conn_id = os.environ["FABRIC_CONNECTION_ID"]  # Ensure the FABRIC_CONNECTION_ID environment variable is set

# Initialize the AIProjectClient with the endpoint and credentials
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Use Azure Default Credential for authentication
    api_version="latest",
)

with project_client:
    # Initialize the FabricTool with the connection ID
    fabric = FabricTool(connection_id=conn_id)

    # Create an agent with the specified model, name, instructions, and tools
    agent = project_client.agents.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=fabric.definitions,  # Tools available to the agent
        headers={"x-ms-enable-preview": "true"},  # Enable preview features
    )
    print(f"Created Agent, ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,  # ID of the thread
        role="user",  # Role of the message sender (e.g., user)
        content="What insights can you provide from the Fabric resource?",  # Message content
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process a run with the specified thread and agent
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Log the error if the run fails
        print(f"Run failed: {run.last_error}")

    # Fetch and log all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages.data:
        print(f"Role: {message.role}, Content: {message.content}")

    # Delete the agent after use
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")