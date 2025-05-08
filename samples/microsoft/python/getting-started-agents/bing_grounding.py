# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
FILE: sample_agents_bing_grounding.py

DESCRIPTION:
    This sample demonstrates how to use agent operations with the Grounding with Bing Search tool from
    the Azure Agents service using a synchronous client.

USAGE:
    python sample_agents_bing_grounding.py

    Before running the sample:

    pip install azure.ai.projects azure-identity

    Set these environment variables with your own values:
    PROJECT_ENDPOINT - the Azure AI Project endpoint, as found in your AI Studio Project.
    AZURE_AI_CONNECTION_ID - the connection ID for the Bing Grounding tool.
    MODEL_DEPLOYMENT_NAME - the deployment name of the AI model.
"""

# Import necessary libraries and modules
import os
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import MessageRole, BingGroundingTool
from azure.ai.projects import AIProjectClient

# Define the project endpoint (replace with your actual project endpoint)
# Example: project_endpoint = "https://<your-ai-services-resource-name>.services.ai.azure.com/api/projects/<your-project-name>"
project_endpoint = os.environ["PROJECT_ENDPOINT"]

# Define the connection ID for the Bing Grounding tool (replace with your actual connection ID)
# Example connection_id= "/subscriptions/<sub-id>/resourceGroups/<your-rg-name>/providers/Microsoft.CognitiveServices/accounts/<your-ai-services-name>/projects/<your-project-name>/connections/<your-bing-connection-name>"
conn_id = os.environ["BING_CONNECTION_NAME"]
print(conn_id)

# Initialize the Bing Grounding tool with the connection ID
bing = BingGroundingTool(connection_id=conn_id)

# Create an AIProjectClient instance to interact with the Azure AI service
project_client = AIProjectClient(
    endpoint=project_endpoint,  # Azure AI service endpoint
    credential=DefaultAzureCredential(),  # Authentication credentials
)

# Use the project client to perform agent operations
with project_client:
    # Create an agent with the specified model, name, instructions, and tools
    agent = project_client.agents.create_agent(
        model= os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=bing.definitions,  # Tools available to the agent
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = project_client.agents.create_thread()
    print(f"Created thread and run, ID: {thread.id}")

    # Create a message in the thread to interact with the agent
    message = project_client.agents.create_message(
        thread_id=thread.id,  # ID of the thread
        role="user",  # Role of the message sender (e.g., user)
        content="what is the weather in Seattle today?",  # Message content
    )
    print(f"Created message: {message['id']}")

    # Create and process an agent run in the thread using the tools
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Check if the run failed and log the error if applicable
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the agent when done to clean up resources
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages in the thread
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")
# </create run>
