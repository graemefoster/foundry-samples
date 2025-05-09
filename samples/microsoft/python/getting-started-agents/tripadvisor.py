# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
FILE: tripadvisor.py

DESCRIPTION:
    This sample demonstrates how to use the Azure AI Agents service to create an agent
    that integrates with the Tripadvisor API. The agent can provide travel recommendations
    such as top-rated hotels, restaurants, and attractions by leveraging the Tripadvisor API.

USAGE:
    python tripadvisor.py

    Before running the sample:

    pip install azure-ai-projects azure-identity

    Set these environment variables with your own values:
    PROJECT_ENDPOINT - The Azure AI Project endpoint, as found in your AI Studio Project.
    MODEL_DEPLOYMENT_NAME - The deployment name of the AI model.
    TRIPADVISOR_CONNECTION_ID - The connection ID for the Tripadvisor API.
"""
# Import necessary libraries for authentication and Azure AI services
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme, OpenApiTool

# Define the endpoint and model deployment name
# Ensure these environment variables are set before running the script
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Azure AI Project endpoint
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # AI model deployment name

# Define the Tripadvisor connection ID
# Ensure this environment variable is set with the correct connection ID
tripadvisor_conn_id = os.environ["TRIPADVISOR_CONNECTION_ID"]  # Azure Tripadvisor connection ID

# Define the OpenAPI specification for the Tripadvisor API
# This includes details about the API endpoints, parameters, and responses
tripadvisor_spec = {
    "openapi": "3.0.1",
    "servers": [
        {
            "url": "https://api.content.tripadvisor.com/api"  # Base URL for the Tripadvisor API
        }
    ],
    "info": {
        "version": "1.0.0",
        "title": "Content API - TripAdvisor(Knowledge)",
        "description": "SSP includes Locations Details, Locations Photos, Locations Reviews, Location Search"
    },
    "paths": {
        "/v1/location/{locationId}/details": {
            "get": {
                "summary": "Location Details",
                "description": "A Location Details request returns comprehensive information about a location (hotel, restaurant, or an attraction) such as name, address, rating, and URLs for the listing on Tripadvisor.",
                "operationId": "getLocationDetails",
                "tags": ["Location Details"],
                "parameters": [
                    {
                        "name": "locationId",
                        "in": "path",
                        "description": "A unique identifier for a location on Tripadvisor. The location ID can be obtained using the Location Search.",
                        "required": True,
                        "schema": {"type": "integer", "format": "int32"}
                    },
                    {
                        "name": "language",
                        "in": "query",
                        "description": "The language in which to return results (e.g. \"en\" for English or \"es\" for Spanish) from the list of our Supported Languages.",
                        "required": False,
                        "schema": {
                            "default": "en",
                            "type": "string",
                            "enum": ["en", "es", "fr", "de", "it", "ja", "zh", "ko", "ru"]
                        }
                    },
                    {
                        "name": "currency",
                        "in": "query",
                        "description": "The currency code to use for request and response (should follow ISO 4217).",
                        "required": False,
                        "schema": {"type": "string", "default": "USD"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Details for the location",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "location_id": {"type": "integer", "format": "int32"},
                                        "name": {"type": "string"},
                                        "description": {"type": "string"},
                                        "web_url": {"type": "string"},
                                        "address_obj": {
                                            "type": "object",
                                            "properties": {
                                                "street1": {"type": "string"},
                                                "city": {"type": "string"},
                                                "state": {"type": "string"},
                                                "country": {"type": "string"},
                                                "postalcode": {"type": "string"}
                                            }
                                        },
                                        "rating": {"type": "number"},
                                        "num_reviews": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                },
                "security": [{"cosoLocationApiLambdaAuthorizer": []}]
            }
        }
    },
    "components": {
        "securitySchemes": {
            "cosoLocationApiLambdaAuthorizer": {
                "type": "apiKey",  # API key-based authentication
                "name": "key",  # Name of the query parameter for the API key
                "in": "query"  # API key is passed as a query parameter
            }
        }
    }
}

# Initialize the AIProjectClient with the endpoint and credentials
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Use Azure Default Credential for authentication
    api_version="latest",
)

with project_client:
    # Initialize the OpenAPI tool for Tripadvisor
    tripadvisor_tool = OpenApiTool(
        name="TripadvisorTool",  # Name of the tool
        description="Tool to access Tripadvisor data for travel recommendations.",  # Description of the tool
        spec=tripadvisor_spec,  # OpenAPI specification
        auth=OpenApiConnectionAuthDetails(
            security_scheme=OpenApiConnectionSecurityScheme(connection_id=tripadvisor_conn_id)  # Authentication details
        ),
    )

    # Create an agent with the specified model, name, instructions, and tools
    agent = project_client.agents.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="tripadvisor-agent",  # Name of the agent
        instructions="You are a helpful travel assistant that uses Tripadvisor data to provide travel guidance.",  # Instructions for the agent
        tools=tripadvisor_tool.definitions,  # Tools available to the agent
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication with the agent
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Can you recommend some top-rated hotels in Paris?",  # Message content
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