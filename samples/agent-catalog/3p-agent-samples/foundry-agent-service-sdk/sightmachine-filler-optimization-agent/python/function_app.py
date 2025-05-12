import azure.functions as func
import logging
import os
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from src.az_fns import data_queue_trigger, name_queue_trigger, pred_queue_trigger

app = func.FunctionApp()


# Name of the queues to get and send the function call messages
name_input_queue_name = "nameinputqueue"
name_output_queue_name = "nameoutputqueue"

data_input_queue_name = "datainputqueue"
data_output_queue_name = "dataoutputqueue"

pred_input_queue_name = "predinputqueue"
pred_output_queue_name = "predoutputqueue"


input_form = """
    <style>
        body {
            font-family: Arial, sans-serif;
        }
    </style>
    <form action="/api/main" method="get">
        <label for="prompt">Your Question:</label><br>
        <textarea id="prompt" name="prompt" rows="4" cols="60" placeholder="Enter your question here" required></textarea><br><br>
        <button type="submit">Ask</button>
    </form>
"""

####
#### Imported and decorated Azure functions for the tools
####


# Data tool
@app.function_name(name="datatool")
@app.queue_trigger(
    arg_name="inputqueue",
    queue_name=data_input_queue_name,
    connection="STORAGE_CONNECTION",
)
@app.queue_output(
    arg_name="outputqueue",
    queue_name=data_output_queue_name,
    connection="STORAGE_CONNECTION",
)
def decorated_data_queue_trigger(
    inputqueue: func.QueueMessage, outputqueue: func.Out[str]
) -> None:
    # Call the data queue trigger function
    data_queue_trigger(inputqueue, outputqueue)


# Name tool
@app.function_name(name="nametool")
@app.queue_trigger(
    arg_name="inputqueue",
    queue_name=name_input_queue_name,
    connection="STORAGE_CONNECTION",
)
@app.queue_output(
    arg_name="outputqueue",
    queue_name=name_output_queue_name,
    connection="STORAGE_CONNECTION",
)
def decorated_name_queue_trigger(
    inputqueue: func.QueueMessage, outputqueue: func.Out[str]
) -> None:
    # Call the name queue trigger function
    name_queue_trigger(inputqueue, outputqueue)


# Prediction tool
@app.function_name(name="predtool")
@app.queue_trigger(
    arg_name="inputqueue",
    queue_name=pred_input_queue_name,
    connection="STORAGE_CONNECTION",
)
@app.queue_output(
    arg_name="outputqueue",
    queue_name=pred_output_queue_name,
    connection="STORAGE_CONNECTION",
)
def decorated_pred_queue_trigger(
    inputqueue: func.QueueMessage, outputqueue: func.Out[str]
) -> None:
    # Call the pred queue trigger function
    pred_queue_trigger(inputqueue, outputqueue)


####
#### End of imported and decorated Azure functions for the tools
####


# Function to initialize the agent client and the tools Azure Functions that the agent can use
def initialize_client_thread():
    # Create a project client using the connection string from local.settings.json
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )

    # Create a thread
    thread = project_client.agents.create_thread()
    logging.info(f"Created thread, thread ID: {thread.id}")

    return project_client, thread


def initialize_name_agent(project_client):
    # Sets up the agent for handling the name tool.
    storage_connection_string = os.environ["STORAGE_CONNECTION__queueServiceUri"]

    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="azure-function-agent-get-name",
        instructions="""
        You are a helpful agent to translate variable names from data on a manufacturing bottling line.
        You do not need to answer the user's question, only translate the variable names and machine names.
        
        The user's request will include variable names and machine names.  These names may not match the names in the database.
        You use the nametool to translate the variable names and machine names to the names in the database.
        Required parameters for the nametool tool function:
        - columns: a list of variable names to be translated, e.g., "Pressure","Temperature","Speed"
        - machines: a list of machine names to be translated, e.g., "Filler_1"
        Returned data will be in the form of a JSON dictionary with the following key/values:
        - "old_name1": "new_name1"
        - "old_name2": "new_name2"
        - "old_machine1": "new_machine1"
        - "old_machine2": "new_machine2"
        etc.
        
        KPI's and metrics do not need to be translated.  Common KPI's and metrics include:
        Throughput, Availability, Yield, USLE, OEE, Efficiency, Quality, Performance, and Losses.
        
        For example, if the user asks, "What is the pressure on Filler 1?" and the database has Press_PV and the machine is named L1_Filler, you should respond with the revised question, "What is the Press_PV on L1_Filler?"
        
        ANSWER:
        Original_question: <user question>
        Revised question: <revised question>
        
        """,
        headers={"x-ms-enable-preview": "true"},
        tools=[
            {
                "type": "azure_function",
                "azure_function": {
                    "function": {
                        "name": "nametool",
                        "description": "Translate column names and machine names to the names found in the database",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "columns": {
                                    "type": "string",
                                    "description": "Comma delimited list of variable names to be renamed.  E.g., 'Pressure,Temperature,Speed'",
                                },
                                "machines": {
                                    "type": "string",
                                    "description": "Comma delimited list of machine names to be renamed.  E.g., 'Filler 1, Filler 2'",
                                },
                            },
                        },
                    },
                    "input_binding": {
                        "type": "storage_queue",
                        "storage_queue": {
                            "queue_service_uri": storage_connection_string,
                            "queue_name": name_input_queue_name,
                        },
                    },
                    "output_binding": {
                        "type": "storage_queue",
                        "storage_queue": {
                            "queue_service_uri": storage_connection_string,
                            "queue_name": name_output_queue_name,
                        },
                    },
                },
            },
        ],
    )
    logging.info(f"Created agent, agent ID: {agent.id}")
    return agent


def initialize_data_pred_agent(project_client):
    # Sets up the agent for handling the data and prediction tools.

    # Get the connection string from local.settings.json
    storage_connection_string = os.environ["STORAGE_CONNECTION__queueServiceUri"]

    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="azure-function-agent-filler-agent",
        instructions="""
        You are a helpful agent to optimize the Filler on a manufacturing bottling line.
        
        
        When the user asks for data use the datatool function.
        Required parameters for the datatool function:
        - columns: a list of columns to query, e.g., "Pressure","Temperature","Speed"
        - machine: the machine to query data for, e.g., "Filler_1"
        - datetime: the datetime in ISO format to query data for, e.g., 2025-01-01T12:00:00Z
        Returned data will be in the form of a json dictionary with a key for each column and a list of values for each column.
        Guidelines for using the datatool function:
        - datetime: The datetime is assumed to be in local time for the machine.  Do not convert it.
        - datetime: To get the most recent data, leave the datetime parameter empty.
        - columns: To get the most important columns, leave the columns field empty.
        - columns: In manufacturing, variables are sometimes called "tags."
        - machine: You must always specify a machine.
        Examples of how to use the datatool function:
            Example, request for specific tags on a specific date:
            {
                "columns": "\"Pressure\",\"Temperature\",\"Speed\"",
                "machine": "Filler_1",
                "datetime": "2025-01-01T12:00:00Z"
            }
            
            Example, request for the most recent data for specific tags:
            {
                "columns": "\"Pressure\",\"Temperature\",\"Speed\"",
                "machine": "Filler_1",
                "datetime": ""
            }
            
            Example, request for the most important data, most recent data:    
            {
                "columns": "",
                "machine": "Filler_1",
                "datetime": ""
            }
            
        When the user asks for predictions or root cause analysis, use the predicttool function.
        Required parameters for the predicttool function:
        - machine: the machine to predict outcome for, e.g., "Filler_1"
        - outcome: the outcome to predict, e.g., "USLE"
        - new_values: a list of new values for the prediction, e.g., "Pressure=10,Temperature=20,Speed=30"
        - datetime: the datetime for the supporting data, in ISO format, e.g., 2025-01-01T12:00:00Z
        - mode: whether to predict or analyze root cause, options are "predict" or "root_cause" or "anomaly"
        Returned data will be in the form of a JSON dictionary with the following key/values:
        - "timestamp": the datetime of the prediction
        - "original": the original value of the outcome
        - "predicted": the predicted value of the outcome, if running a predictions
        - "causes": a list of most important variables that caused the outcome, if running root cause analysis
        - "tag_name": the name of the variable that was changed
        - "outcome": the outcome that was predicted
        Guidelines for using the predicttool function:
        - machine: You must always specify a machine.
        - datetime: The datetime is assumed to be in local time for the machine.  Do not convert it.
        - datetime: To use the most recent data, leave the datetime parameter empty.
        - new_values: You do not need to specify all variables, only the ones you want to change.
        - new_values: You do not need to specify new values when doing root cause analysis.
        - new values: You can specify absolute new values or a percentage of the original.  For example, "Pressure=110%" will predict if pressure was 10 percent higher.
        Examples of how to use the predicttool function:
            Example, request for a prediction with new values based on most recent data:
            {
                "machine": "Filler_1",
                "outcome": "USLE",
                "new_values": "Speed=30",
                "mode": "predict"
            }

            Example, request for a root cause analysis with no new values:
            {
                "machine": "Filler_1",
                "outcome": "USLE",
                "datetime": "2025-01-01T12:00:00Z",
                "mode": "root_cause"
            }
        
        If you do not have enough information to answer the question, ask for more information.
        If you do not know the answer, say you do not know.
        
        You do not need to repeat the question in your answer.
        If you retrieve data, provide a brief summary of the data retrieved.
        If you make a prediction, provide the original value, the predicted value, and the new values used for the prediction.
        Answer in a narrative format, but include a table when appropriate.
        
        Answer in the following format:
        Approach: <approach used>
        Data and results: <data/results retrieved>
        
        
        """,
        headers={"x-ms-enable-preview": "true"},
        tools=[
            {
                "type": "azure_function",
                "azure_function": {
                    "function": {
                        "name": "predtool",
                        "description": "Predictions, anomaly detection and root cause analysis for filler machine.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "machine": {
                                    "type": "string",
                                    "description": "The machine to query data for, e.g., 'Filler_1'.",
                                },
                                "outcome": {
                                    "type": "string",
                                    "description": "The KPI being optimized, e.g., USLE, Availability, Yield",
                                },
                                "new_values": {
                                    "type": "string",
                                    "description": "A list of new values for the prediction, e.g., 'Pressure=10'.  Can provide absolute values or a percentage, such as 'Pressure=110%'",
                                },
                                "datetime": {
                                    "type": "string",
                                    "description": "The datetime in ISO format to query data for.  E.g., 2025-01-01T12:00:00Z",
                                },
                                "mode": {
                                    "type": "string",
                                    "description": "The mode of the prediction, either 'predict', 'root_cause', or anomaly.",
                                },
                            },
                            "required": ["machine"],
                        },
                    },
                    "input_binding": {
                        "type": "storage_queue",
                        "storage_queue": {
                            "queue_service_uri": storage_connection_string,
                            "queue_name": pred_input_queue_name,
                        },
                    },
                    "output_binding": {
                        "type": "storage_queue",
                        "storage_queue": {
                            "queue_service_uri": storage_connection_string,
                            "queue_name": pred_output_queue_name,
                        },
                    },
                },
            },
            {
                "type": "azure_function",
                "azure_function": {
                    "function": {
                        "name": "datatool",
                        "description": "Get data for a manufacturing bottling line.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "columns": {
                                    "type": "string",
                                    "description": """list of columns, each enclosed in quotes, separated by commas.  E.g., "Pressure","Temperature","Speed" """,
                                },
                                "machine": {
                                    "type": "string",
                                    "description": "The machine to query data for, e.g., 'Filler_1'.",
                                },
                                "datetime": {
                                    "type": "string",
                                    "description": "The datetime in ISO format to query data for.  E.g., 2025-01-01T12:00:00Z",
                                },
                            },
                            "required": ["machine"],
                        },
                    },
                    "input_binding": {
                        "type": "storage_queue",
                        "storage_queue": {
                            "queue_service_uri": storage_connection_string,
                            "queue_name": data_input_queue_name,
                        },
                    },
                    "output_binding": {
                        "type": "storage_queue",
                        "storage_queue": {
                            "queue_service_uri": storage_connection_string,
                            "queue_name": data_output_queue_name,
                        },
                    },
                },
            },
        ],
    )
    logging.info(f"Created agent, agent ID: {agent.id}")
    return agent


def ask_question(message_text, project_client, thread, agent):
    # Send the message to the agent
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=message_text,
    )
    logging.info(f"Created message, message ID: {message.id}")

    # Run the agent
    run = project_client.agents.create_run(
        thread_id=thread.id, agent_id=agent.id, parallel_tool_calls=False
    )
    # Monitor and process the run status
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

        if run.status not in ["queued", "in_progress", "requires_action"]:
            break

    logging.info(f"Run finished with status: {run.status}")

    if run.status == "failed":
        logging.error(f"Run failed: {run.last_error}")
        return None

    messages = project_client.agents.list_messages(thread_id=thread.id)
    logging.info(f"Messages: {messages}")

    # Get the last message from the agent
    last_msg = None
    for data_point in messages.data:
        if data_point.role == "assistant":
            last_msg = data_point.content[-1]
            logging.info(f"Last Message: {last_msg.text.value}")
            break

    return last_msg.text.value


@app.route(route="main", auth_level=func.AuthLevel.FUNCTION)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Get the prompt from the URL query parameters
    user_question = req.params.get("prompt")
    if not user_question:
        return func.HttpResponse(input_form, mimetype="text/html")

    prompt = user_question

    # Initialize the agent client
    project_client, thread = initialize_client_thread()
    name_agent = initialize_name_agent(project_client)
    data_pred_agent = initialize_data_pred_agent(project_client)

    # Split naming into separate step to increase reliability of response
    naming_response = ask_question(prompt, project_client, thread, name_agent)
    # From the naming response, extract the second line, and the text after the colon

    try:
        revised_question = naming_response.split("\n")[2].split(":")[1].strip()
    except Exception as e:
        # GPT gave an inconsistent response, so let the next step try handle it
        revised_question = naming_response

    logging.info(f"Revised question: {revised_question}")

    # revised_question += "Format your answer as html, and only use html.  Do not enclose the answer in ```html and ```.  Do not include other text not in html."

    response = ask_question(revised_question, project_client, thread, data_pred_agent)

    # Delete the agent once done
    project_client.agents.delete_agent(data_pred_agent.id)
    project_client.agents.delete_agent(name_agent.id)
    logging.info("Deleted agents")

    response_html = input_form
    # take the portion of the prompt through the question mark
    response_html += f"<p><p><b>Question:</b>{user_question}?"

    if response:
        response_html += f"<p><pre>{response}</pre></p>"
    else:
        response_html += "<p>No response from agent.</p>"

    return func.HttpResponse(response_html, mimetype="text/html", status_code=200)
