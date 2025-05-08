# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
FILE: agent_sharepoint.py

DESCRIPTION:
    This sample demonstrates how to use agent operations with the SharePoint tool from
    the Azure Agents service using a synchronous client.

USAGE:
    python agent_sharepoint.py

    Before running the sample:

    pip install azure.ai.projects azure-identity

    Set these environment variables with your own values:
    PROJECT_ENDPOINT - the Azure AI Project endpoint, as found in your AI Studio Project.
    MODEL_DEPLOYMENT_NAME - the deployment name of the AI model.
    CONNECTION_NAME - the name of the SharePoint connection.
"""

import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import SharepointTool
from azure.identity import DefaultAzureCredential

# Retrieve endpoint and model deployment name from environment variables
endpoint = os.environ["PROJECT_ENDPOINT"],  # Ensure the PROJECT_ENDPOINT environment variable is set
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # Ensure the MODEL_DEPLOYMENT_NAME environment variable is set

# Initialize the AIProjectClient with the endpoint and credentials
with AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Use Azure Default Credential for authentication
) as project_client:
    # Initialize SharePoint tool with connection ID
    sharepoint_connection = project_client.connections.get(
        name="CONNECTION_NAME",  # Replace with your actual connection name
    )
    conn_id = sharepoint_connection.id  # Retrieve the connection ID
    print(conn_id)
    sharepoint = SharepointTool(connection_id=conn_id)  # Initialize the SharePoint tool with the connection ID
    
    # Access the agents client from the project client
    agents_client = project_client.agents
    
    # Create an agent with the specified model, name, instructions, and tools
    agent = agents_client.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=sharepoint.definitions,  # Tools available to the agent
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = agents_client.create_thread()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = agents_client.create_message(
        thread_id=thread.id,  # ID of the thread
        role="user",  # Role of the message sender (e.g., user)
        content="Hello, summarize the key points of the <sharepoint_resource_document>",  # Message content
    )
    print(f"Created message, ID: {message.id}")

    # Create and process an agent run in the thread using the tools
    run = agents_client.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Log the error if the run fails
        print(f"Run failed: {run.last_error}")

    # Delete the agent when done to clean up resources
    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages from the thread
    messages = agents_client.list_message(thread_id=thread.id)
    for msg in messages:
        if msg.text_messages:  # Check if there are text messages
            last_text = msg.text_messages[-1]  # Get the last text message
            print(f"{msg.role}: {last_text.text.value}")  # Print the role and message content

