# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
FILE: azure_ai_search.py

DESCRIPTION:
    This sample demonstrates how to use agent operations with the Azure AI Search tool from
    the Azure Agents service using a synchronous client.

USAGE:
    python azure_ai_search.py

    Before running the sample:

    pip install azure.ai.projects azure-identity

    Set these environment variables with your own values:
    PROJECT_ENDPOINT - the Azure AI Project endpoint, as found in your AI Studio Project.
    MODEL_DEPLOYMENT_NAME - the deployment name of the AI model.
    AZURE_AI_CONNECTION_ID - the connection ID for the Azure AI Search tool.
"""

# Import necessary libraries and modules
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import AzureAISearchQueryType, AzureAISearchTool, ListSortOrder, MessageRole
from azure.identity import DefaultAzureCredential

# Define the Azure AI Search connection ID (replace with your actual connection ID)
azure_ai_conn_id = os.environ["AZURE_AI_CONNECTION_ID"]

# Initialize the Azure AI Search tool with the required parameters
ai_search = AzureAISearchTool(
    index_connection_id=azure_ai_conn_id,  # Connection ID for the Azure AI Search index
    index_name="sample_index",            # Name of the search index
    query_type=AzureAISearchQueryType.SIMPLE,  # Query type (e.g., SIMPLE, FULL)
    top_k=3,                              # Number of top results to retrieve
    filter=""                             # Optional filter for search results
)

# Define the endpoint and model deployment name (replace with your actual values)
endpoint = os.environ["PROJECT_ENDPOINT"],
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]

# Create an AIProjectClient instance to interact with the Azure AI service
with AIProjectClient(
    endpoint=endpoint,  # Azure AI service endpoint
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Authentication credentials
) as project_client:
    # Access the agents client from the project client
    agents_client = project_client.agents

    # Create an agent with the specified model, name, instructions, and tools
    agent = agents_client.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="my-agent",              # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=ai_search.definitions,  # Tools available to the agent
        tool_resources=ai_search.resources,  # Resources for the tools
    )
    # [END create_agent_with_azure_ai_search_tool]
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = agents_client.create_thread()
    print(f"Created thread, ID: {thread.id}")

    # Create a message in the thread to interact with the agent
    message = agents_client.create_message(
        thread_id=thread.id,  # ID of the thread
        role="user",          # Role of the message sender (e.g., user)
        content="What is the temperature rating of the cozynights sleeping bag?",  # Message content
    )
    print(f"Created message, ID: {message.id}")

    # Create and process an agent run in the thread using the tools
    run = agents_client.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Check if the run failed and log the error if applicable
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch and log the details of the agent run steps
    run_steps = agents_client.list_run_steps(thread_id=thread.id, run_id=run.id)
    for step in run_steps.data:
        print(f"Step {step['id']} status: {step['status']}")
        step_details = step.get("step_details", {})
        tool_calls = step_details.get("tool_calls", [])

        # Log details of tool calls if available
        if tool_calls:
            print("  Tool calls:")
            for call in tool_calls:
                print(f"    Tool Call ID: {call.get('id')}")
                print(f"    Type: {call.get('type')}")

                azure_ai_search_details = call.get("azure_ai_search", {})
                if azure_ai_search_details:
                    print(f"    azure_ai_search input: {azure_ai_search_details.get('input')}")
                    print(f"    azure_ai_search output: {azure_ai_search_details.get('output')}")
        print()  # Add an extra newline between steps

    # Delete the agent when done to clean up resources
    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    # [START populate_references_agent_with_azure_ai_search_tool]
    # Fetch and log all messages in the thread
    messages = agents_client.list_messages(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages.data:
        # Log agent messages with URL citation annotations
        if message.role == MessageRole.AGENT and message.url_citation_annotations:
            placeholder_annotations = {
                annotation.text: f" [see {annotation.url_citation.title}] ({annotation.url_citation.url})"
                for annotation in message.url_citation_annotations
            }
            for message_text in message.text_messages:
                message_str = message_text.text.value
                for k, v in placeholder_annotations.items():
                    message_str = message_str.replace(k, v)
                print(f"{message.role}: {message_str}")
        else:
            # Log other messages without annotations
            for message_text in message.text_messages:
                print(f"{message.role}: {message_text.text.value}")
    # [END populate_references_agent_with_azure_ai_search_tool]
