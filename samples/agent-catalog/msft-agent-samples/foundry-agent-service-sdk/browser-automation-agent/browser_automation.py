# pylint: disable=line-too-long,useless-suppression
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
DESCRIPTION:
    This sample demonstrates how to use browser automation agent operations from
    the Azure Agents service using a synchronous client.
 
USAGE:
    python browser_automation.py
 
    Before running the sample:
 
    pip install azure-ai-projects azure-identity
 
    Set these environment variables with your own values:
    1) PROJECT_CONNECTION_STRING - The project connection string, as found in the overview page of your
       Azure AI Foundry project.
    2) MODEL_DEPLOYMENT_NAME - The deployment name of the AI model, as found under the "Name" column in 
       the "Models + endpoints" tab in your Azure AI Foundry project.
    3) PLAYWRIGHT_CONNECTION_ID (Optional) - The connection ID of the Serverless connection containing the details
         of the Playwright browser. If not provided, a MSFT managed playwright resource will be used.
         Format: <AI Project resource ID>/connections<Serverless connection name>
         - Creating a Microsoft Playwright Resource: https://learn.microsoft.com/en-us/azure/playwright-testing/how-to-manage-playwright-workspace?tabs=playwright
         - Give the Project Identity a "Contributor" role on the Playwright resource.
         - Generate an API Key for the Playwright resource: https://learn.microsoft.com/en-us/azure/playwright-testing/how-to-manage-access-tokens
         - Create a serverless connection in the Azure AI Foundry project with the Playwright endpoint and Access Key. 
"""

# <imports>
from os import environ, getenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageRole
from azure.identity import DefaultAzureCredential
from typing import Any, Dict
# </imports>

# <client_initialization>
endpoint = environ["PROJECT_ENDPOINT"]
model_deployment_name = environ["MODEL_DEPLOYMENT_NAME"]
with AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
) as project_client:
# </client_initialization>
    playwright_connection_id: str | None = getenv("PLAYWRIGHT_CONNECTION_ID")

    # [START create_agent_with_browser_automation_tool]
    # <browser_automation_tool_setup>
    browser_automation_tool_definition: Dict[str, Any] = {
        "type": "browser_automation",
    }
    if playwright_connection_id:
        browser_automation_tool_definition["browser_automation"] = {
            "connection": {
                "id": playwright_connection_id,
            }
        }
    
    payload: Dict[str, Any] = {
        "name": "Browser Automation Tool Demo Agent",
        "description": "A demo agent that uses the browser automation tool.",
        "model": model_deployment_name,
        "instructions": "You are an agent to help me with browser automation tasks. You can answer questions, provide information, and assist with various tasks related to web browsing using the browser_automation tool available to you.",
        "tools": [browser_automation_tool_definition],
    }
    # </browser_automation_tool_setup>
    # <agent_creation>
    agent = project_client.agents.create_agent(
        body=payload,
    )
    print(f"Created agent, agent ID: {agent.id}")
    # [END create_agent_with_browser_automation_tool]
    # </agent_creation>

    # <thread_management>
    # Create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Find a popular quinoa salad recipe on Allrecipes with more than 500 reviews and a rating above 4 stars. Create a shopping list of ingredients for this recipe and include the total cooking and preparation time. on https://www.allrecipes.com/",
    )
    print(f"Created message, message ID: {message.id}")
    # </thread_management>

    # <message_processing>
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Get messages from the thread
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")

    # Get the last message from agent
    last_msg = messages.get_last_text_message_by_role(MessageRole.AGENT)
    if last_msg:
        print(f"Last Message: {last_msg.text.value}")
    # </message_processing>

    # <cleanup>
    # Delete the agent once done
    result = project_client.agents.delete_agent(agent.id)
    if result.deleted:
        print(f"Deleted agent {result.id}")
    else:
        print(f"Failed to delete agent {result.id}")
    # </cleanup>
