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

# Retrieve the endpoint and model deployment name from environment variables
endpoint = os.environ["PROJECT_ENDPOINT"]  # Azure AI service endpoint
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # AI model deployment name

# [START create_agent_with_fabric_tool]
# Retrieve the Fabric connection ID from environment variables
conn_id = os.environ["FABRIC_CONNECTION_ID"]
print(conn_id)

# Initialize the FabricTool with the connection ID
fabric = FabricTool(connection_id=conn_id)

# Create an AIProjectClient instance to interact with the Azure AI service
with AIProjectClient(
    endpoint=endpoint,  # Azure AI service endpoint
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Authentication credentials
) as project_client:
    
    # Access the AgentsClient from the AIProjectClient
    agents_client = project_client.agents

    # Create an agent with the specified model, name, instructions, tools, and headers
    agent = agents_client.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=fabric.definitions,  # Tools available to the agent
        headers={"x-ms-enable-preview": "true"},  # Enable preview features
    )
    # [END create_agent_with_fabric_tool]
    print(f"Created Agent, ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = agents_client.create_thread()
    print(f"Created thread, ID: {thread.id}")

    # Create a message in the thread to interact with the agent
    message = agents_client.create_message(
        thread_id=thread.id,  # ID of the thread
        role="user",  # Role of the message sender (e.g., user)
        content="<User query against Fabric resource>",  # Message content
    )
    print(f"Created message, ID: {message.id}")

    # Create and process an agent run in the thread using the tools
    run = agents_client.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Check if the run failed and log the error if applicable
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the agent when done to clean up resources
    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages in the thread
    messages = agents_client.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")