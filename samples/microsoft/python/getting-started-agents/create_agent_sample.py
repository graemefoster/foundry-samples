# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
FILE: create_agent_sample.py

DESCRIPTION:
    This sample demonstrates how to create an agent using the Azure AI Agents service
    with an authenticated AIProjectClient.

USAGE:
    python create_agent_sample.py

    Before running the sample:

    pip install azure-ai-projects azure-ai-agents azure-identity

    Set these environment variables with your own values:
    PROJECT_ENDPOINT - The Azure AI Project endpoint, as found in the overview page of your
                       Azure AI Foundry project.
    MODEL_DEPLOYMENT_NAME - The AI model deployment name, to be used by your Agent, as found
                            in your AI Foundry project.
"""

# Import necessary libraries and modules
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Define the endpoint and model deployment name (replace with your actual values)
endpoint = os.environ["PROJECT_ENDPOINT"]  # Example: endpoint = "https://<your-ai-services-resource-name>.services.ai.azure.com/api/projects/<your-project-name>"# Example: model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"] # Replace with your model deployment name

# Create an AIProjectClient instance to interact with the Azure AI service
with AIProjectClient(
    endpoint=endpoint,  # Azure AI service endpoint
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Authentication credentials
) as project_client:

    # [START agents_sample]
    # Create an agent with the specified model, name, and instructions
    agent = project_client.agents.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are helpful agent",  # Instructions for the agent
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Do something with your Agent!
    # For example, create a thread for communication with the agent

    # Delete the agent when done to clean up resources
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
    # [END connection_sample]