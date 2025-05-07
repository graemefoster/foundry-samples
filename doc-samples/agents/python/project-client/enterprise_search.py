# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
FILE: enterprise_search.py

DESCRIPTION:
    This sample demonstrates how to use agent operations with the Code Interpreter tool from
    the Azure Agents service using a synchronous client.

USAGE:
    python enterprise_search.py

    Before running the sample:

    pip install azure-ai-agents azure-identity

    Set these environment variables with your own values:
    1) PROJECT_ENDPOINT - The Azure AI Agents endpoint.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
"""

# Import necessary libraries and modules
import os
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    CodeInterpreterTool,  # Tool for enabling code interpretation capabilities
    MessageAttachment,  # Represents an attachment to a message
    VectorStoreDataSource,  # Data source for vector store creation
    VectorStoreDataSourceAssetType,  # Enum for specifying the type of vector store asset
)
from azure.identity import DefaultAzureCredential  # For authentication
from azure.ai.projects import AIProjectClient  # Client to interact with Azure AI Projects

# Retrieve the endpoint and model deployment name from environment variables
endpoint = os.environ["PROJECT_ENDPOINT"]  # Azure AI service endpoint
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # AI model deployment name

# Create an AIProjectClient instance to interact with the Azure AI service
with AIProjectClient(
    endpoint=endpoint,  # Azure AI service endpoint
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Authentication credentials
) as project_client:
    
    # Access the AgentsClient from the AIProjectClient
    agents_client = project_client.agents

    # Initialize the CodeInterpreterTool for enabling code interpretation
    code_interpreter = CodeInterpreterTool()

    # Create an agent with the specified model, name, instructions, and tools
    # Note: CodeInterpreter must be enabled in the agent creation for file attachment support
    agent = agents_client.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are helpful agent",  # Instructions for the agent
        tools=code_interpreter.definitions,  # Tools to be used by the agent
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = agents_client.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # [START upload_file_and_create_message_with_code_interpreter]
    # We will upload the local file to Azure and will use it for vector store creation.
    asset_uri = os.environ["AZURE_BLOB_URI"]
    ds = VectorStoreDataSource(asset_identifier=asset_uri, asset_type=VectorStoreDataSourceAssetType.URI_ASSET)

    # Create a message with the attachment
    attachment = MessageAttachment(data_source=ds, tools=code_interpreter.definitions)
    message = agents_client.create_message(
        thread_id=thread.id, role="user", content="What does the attachment say?", attachments=[attachment]
    )
    # [END upload_file_and_create_message_with_code_interpreter]

    print(f"Created message, message ID: {message.id}")

    # Create and process a run with the specified thread and agent
    run = agents_client.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Check if the run failed and print the error message if so
    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # Delete the agent after use
    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    # List and print all messages in the thread
    messages = agents_client.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")