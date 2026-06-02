import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    AzureFunctionAgentTool,
    AzureFunctionDefinition,
    AzureFunctionDefinitionFunction,
    AzureFunctionBinding,
    AzureFunctionStorageQueue
)
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize logging for Application Insights
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Get endpoint and model from environment variables
endpoint = os.getenv("PROJECT_ENDPOINT") or os.getenv("AZURE_AI_PROJECT_ENDPOINT") or ""
model = os.getenv("MODEL_DEPLOYMENT_NAME") or os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME") or "gpt-4o"

# Storage account configuration for the Azure Function queue bindings
storage_service_endpoint = os.getenv("STORAGE_SERVICE_ENDPOINT") or ""

# Initialize client

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

with project_client:

    openai_client = project_client.get_openai_client()

    # Define Azure Function tool (v2.x structure matching v1.x addition_qtfnc)
    # - Agent writes to input_binding queue (add-queue)
    # - Azure Function reads from input queue, processes, writes to output queue
    # - Agent reads response from output_binding queue (add-result-queue)
    function_tool = AzureFunctionAgentTool(
        azure_function=AzureFunctionDefinition(
            function=AzureFunctionDefinitionFunction(
                name="weather_forecast",
                description="Gets the weather forecast for a given location.",
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Location to get the weather forecast for"},
                        "outputqueueuri": {
                            "type": "string",
                            "description": "The full output queue uri.",
                        },
                        "CorrelationId": {
                            "type": "string",
                            "description": "The correlation ID for tracking the request.",
                        },
                    },
                    "required": ["location", "outputqueueuri", "CorrelationId"]
                }
            ),
            input_binding=AzureFunctionBinding(
                storage_queue=AzureFunctionStorageQueue(
                    queue_service_endpoint=storage_service_endpoint,
                    queue_name="inputqueuetest"
                )
            ),
            output_binding=AzureFunctionBinding(
                storage_queue=AzureFunctionStorageQueue(
                    queue_service_endpoint=storage_service_endpoint,
                    queue_name="outputqueuetest",
                )
            )
        )
    )

    agent = project_client.agents.create_version(
        agent_name="basic-agent-fc-fa",
        definition=PromptAgentDefinition(
            model=model,
            instructions=f"You are a helpful assistant. Use the tool to find the weather. ALWAYS specify the output queue uri parameter as '{storage_service_endpoint}/add-result-queue'.",
            tools=[function_tool],
        ),
        description="Agent with Azure Function tool for addition",
    )

    logger.info(f"Agent created with ID: {agent.id}")

    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    conversation = openai_client.conversations.create(
        items=[
            {"type": "message", "role": "user", "content": "What is the weather in Adelaide?"},
        ],
    )   

    # Get response from the agent (Responses API - stateless)
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
        input="",
    )
    print(f"Response output: {response.output_text}")
    logger.info(f"Response output: {response.output_text}")

    # Cleanup: delete the agent version
    # project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    logger.info(f"Agent deleted: {agent.name} version {agent.version}")
    print(f"Agent deleted: {agent.name} version {agent.version}")



 