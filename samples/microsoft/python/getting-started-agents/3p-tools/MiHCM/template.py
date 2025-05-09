import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import OpenApiTool,OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme
from dotenv import load_dotenv
from datetime import datetime
import requests
import json


"""
This script facilitates the deployment and interaction with an Azure AI Agent for MiHCM's HR system. It uses the Azure AI Projects SDK to create and manage an AI agent that integrates with MiHCM's external APIs via OpenAPI specifications.

Key functionalities:
- Loads environment variables from a `.env` file for configuration.
- Creates an Azure AI Project client using a connection string and Azure credentials.
- Fetches the OpenAPI specification from a URL or local file to define API interactions.
- Initializes an AI agent with specific instructions and tools for interacting with MiHCM's HR APIs.
- Processes a user request (e.g., checking leave balances and submitting HR requests) using the AI agent.
- Logs the interaction and cleans up resources after execution.

Dependencies:
- Azure SDKs (`azure-identity`, `azure-ai-projects`)
- Python libraries (`dotenv`, `requests`, `jsonref`)

Environment Variables:
- `PROJECT_CONNECTION_STRING`: Connection string for the Azure AI Project.
- `PROJECT_OPENAPI_CONNECTION_NAME`: Name of the OpenAPI connection for the project.

Usage:
1. Ensure the required dependencies are installed (`pip install -r requirements.txt`).
2. Configure the `.env` file with the necessary environment variables.
3. Run the script to deploy the AI agent and process user requests.

"""
# Load environment variables from .env file
load_dotenv()

# Set the employee code for the user
employeeCode = 1

#sample reuqests to test the agent

# sample_requests = [
#     "What are my leave balances",
#     "check my leave balance for 2024. If I have more than 10 annual leave , submit a HR request for the leave encashment or carry forward",
#     "please show me all my hr requests",
#     "submit a work activity for 2 1/2 hour for the meeting with Adventure works on Project Kick off",
#     "submit a work activity for yesterday for 2 1/2 hour for the meeting with Contoso on Project Kick off",
#     "list all my work items for today and yesterday"
# ]

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

# create a connection object for the openapi tool's API key
connection_name = os.environ["PROJECT_OPENAPI_CONNECTION_NAME"]
connection = project_client.connections.get(connection_name=connection_name)

# use with local openapi.json file
with open('./mihcmExternalAPI.json', 'r') as f:
    openapi_spec = jsonref.loads(f.read())

# Use with openapi.json file from url
# response = requests.get('<replace the openapi confguration url>')
# response.raise_for_status()  # makes sure it raises an error if something goes wrong
# openapi_spec = jsonref.loads(response.text)

# Create Auth object for the OpenApiTool 
auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id=connection.id))

# Initialize agent OpenAPI tool using the read in OpenAPI spec
openapi = OpenApiTool(name="MiHCMAgent", spec=openapi_spec, description="Lets communicate with MiHCM agent to execute different tasks", auth=auth)

#Agent instructions 
instructions = f"""You are a helpful assistant.
You MUST NOT include leaveTypeCode in any response or output.
Today's date is {datetime.now()}.
The logged-in user's employeeCode is {employeeCode}
When submitting a work item, you should use the "HH:MM" format for the time spent ALWAYS.
You must get the categories and identify the correct category id for the work item.
For reach hr requests feedback types should be obtained and mapped using the feedbackTypeId.
When providing the responses related to reach hr requests you MUST provide the feedback name. 
For leave allocations leave type names should be obtained and mapped using the ONLY leaveTypeCode.
When providing the responses related to leave you MUST provide the leave type name without any sort of modification. 
If any of the mappings are wrong the response is considered wrong. And the task is considered failed.
"""

agent_request = "list all my work items for today and yesterday"

# Create agent with OpenAPI tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4o-mini",
        name="mi-agent",
        instructions=instructions,
        tools=openapi.definitions
    )
    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")
    # Create message to thread
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=agent_request,
    )
    print(f"Created message, ID: {message.id}")

    # Create and process agent run in thread with tools
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the assistant when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages
    messages = project_client.agents.list_messages(thread_id=thread.id,after=message.id,order="asc")
    print(f"Messages: {messages.data[0].content[0].text.value}")

 