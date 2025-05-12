# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use LEGALFLY from
    the Azure AI Agent service using a synchronous client.

USAGE:
    python main.py

    Before running the sample:

    pip install azure-ai-projects azure-ai-agents azure-identity python-dotenv

    Set these environment variables with your own values:
    1) PROJECT_CONNECTION_STRING - the Azure AI Agents connection string.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in
       the "Models + endpoints" tab in your Azure AI Foundry project.
    3) LEGALFLY_API_CONNECTION_NAME - The name of the connection for the LegalFly API.
"""
# <initialization>
# Import necessary libraries
import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import OpenApiTool, OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
connection_string = os.environ["PROJECT_CONNECTION_STRING"]
model = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o")
connection_name = os.environ["LEGALFLY_API_CONNECTION_NAME"]

# Initialize the project client using the connection string and default credentials
project = AIProjectClient.from_connection_string(
    connection_string,
    DefaultAzureCredential()
)

# Fetch the OpenAPI spec from the LegalFly public URL
with open("./legalfly.json", "r") as f:
    openapi_spec = jsonref.loads(f.read())

connection = project.connections.get(connection_name=connection_name)
print(f"Created connection, connection ID: {connection.id}")

auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id=connection.id))

openapi_tool = OpenApiTool(
    name="getLegalCounsel",
    spec=openapi_spec,
    description="LegalFly legal counsel API",
    auth=auth
)

agent = project.agents.create_agent(
    model=model,
    name="my-agent",
    instructions="You are a helpful AI legal assistant. Act like a friendly person who possesses a lot of legal knowledge.",
    tools=openapi_tool.definitions,
)
print(f"Created agent, agent ID: {agent.id}")

thread = project.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

message = project.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="What do I need to start a company in California?",
)
print(f"Created message, message ID: {message.id}")

run = project.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")


if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Print the messages from the agent, from oldest to newest
messages = project.agents.list_messages(thread_id=thread.id)
messages_array = messages.data
for m in messages_array:
    content = m.get("content", [])
    if content and content[0].get("type") == "text":
        text_value = content[0].get("text", {}).get("value", "")
        print(f"Text: {text_value}")

# Delete the agent once done
project.agents.delete_agent(agent.id)
print("Deleted agent")
