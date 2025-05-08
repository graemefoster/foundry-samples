# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
FILE: file_search.py

DESCRIPTION:
    This sample demonstrates how to use agent operations with the File Search tool from
    the Azure Agents service using a synchronous client.

USAGE:
    python file_search.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    PROJECT_ENDPOINT - The Azure AI Project endpoint, as found in your AI Studio Project.
    MODEL_DEPLOYMENT_NAME - The deployment name of the AI model.
"""

import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import (
    FileSearchTool,
    FilePurpose,
)
from azure.identity import DefaultAzureCredential

# Define the path to the asset file to be uploaded
asset_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/product_info_1.md"))

# Retrieve environment variables for endpoint and model deployment name
endpoint = os.environ["PROJECT_ENDPOINT"],  # Ensure the environment variable is set
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # Ensure the environment variable is set

# Initialize the AIProjectClient with the endpoint and credentials
with AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
) as project_client:
    
    # Access the agents client from the project client
    agents_client = project_client.agents
    
    # Upload the file and specify its purpose
    file = agents_client.upload_file_and_poll(file_path=asset_file_path, purpose=FilePurpose.AGENTS)
    print(f"Uploaded file, file ID: {file.id}")

    # Create a vector store using the uploaded file
    vector_store = agents_client.create_vector_store_and_poll(file_ids=[file.id], name="my_vectorstore")
    print(f"Created vector store, vector store ID: {vector_store.id}")

    # Create a file search tool using the vector store
    file_search = FileSearchTool(vector_store_ids=[vector_store.id])

    # Create an agent with the specified model, name, instructions, and tools
    agent = agents_client.create_agent(
        model=model_deployment_name,
        name="my-agent",
        instructions="Hello, you are helpful agent and can search information from uploaded files",
        tools=file_search.definitions,
        tool_resources=file_search.resources,
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = agents_client.create_thread()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = agents_client.create_message(
        thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?"
    )
    print(f"Created message, ID: {message.id}")

    # Create and process an agent run in the thread
    run = agents_client.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Log the error if the run fails
        print(f"Run failed: {run.last_error}")

    # Cleanup resources after use
    # Delete the vector store
    agents_client.delete_vector_store(vector_store.id)
    print("Deleted vector store")

    # Delete the uploaded file
    agents_client.delete_file(file_id=file.id)
    print("Deleted file")

    # Delete the agent
    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages from the thread
    messages = agents_client.list_messages(thread_id=thread.id)

    # Print messages from the thread
    for text_message in messages.text_messages:
        print(text_message)