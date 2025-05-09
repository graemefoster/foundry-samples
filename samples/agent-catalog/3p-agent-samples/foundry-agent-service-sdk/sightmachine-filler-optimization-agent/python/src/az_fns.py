import os
import json
import logging
from datetime import datetime

import pandas as pd
import azure.functions as func

###
### Set of azure functions for user with the Filler AI Agent
### This is a set of stub functions for proof of concept
### For full production code that accesses Sight Machine,
### Please contact us via https://sightmachine.com/contact/
###


def data_queue_trigger(
    inputqueue: func.QueueMessage, outputqueue: func.Out[str]
) -> None:

    logging.info(
        "Python Queue trigger processed a message: %s",
        inputqueue.get_body().decode("utf-8"),
    )

    # Get user input information
    messagepayload = json.loads(inputqueue.get_body().decode("utf-8"))
    column_names = messagepayload.get("columns", "")
    machine_name = messagepayload.get("machine", "")
    timestamp = messagepayload.get("datetime", "")
    correlation_id = messagepayload["CorrelationId"]

    if column_names == "Throughput":
        data = {"Throughput (BPM)": [251]}
    else:
        data = {col: [102] for col in column_names.split(",")}

    # Send message to queue. Sends a mock message for the weather
    result_message = {
        "Value": f"Data for {machine_name} at {timestamp}: {data}",
        "CorrelationId": correlation_id,
    }
    outputqueue.set(json.dumps(result_message).encode("utf-8"))

    logging.info(
        "Sent message to queue: nameoutputqueue with message %s", result_message
    )


def name_queue_trigger(
    inputqueue: func.QueueMessage, outputqueue: func.Out[str]
) -> None:

    logging.info(
        "Python Queue trigger processed a message: %s",
        inputqueue.get_body().decode("utf-8"),
    )

    # Get user input information
    messagepayload = json.loads(inputqueue.get_body().decode("utf-8"))
    column_names = messagepayload.get("columns", "")
    machine_names = messagepayload.get("machines", "")
    correlation_id = messagepayload["CorrelationId"]

    column_names = {col: "Pressure_PV" for col in column_names.split(",")}
    machine_names = {mach: "L1_Filler" for mach in machine_names.split(",")}

    renamed_pairs = column_names.copy()
    renamed_pairs.update(machine_names)

    result_message = {
        "Value": str(renamed_pairs),
        "CorrelationId": correlation_id,
    }
    outputqueue.set(json.dumps(result_message).encode("utf-8"))

    logging.info(
        "Sent message to queue: nameoutputqueue with message %s", result_message
    )


def pred_queue_trigger(
    inputqueue: func.QueueMessage, outputqueue: func.Out[str]
) -> None:

    logging.info(
        "Python Queue trigger processed a message: %s",
        inputqueue.get_body().decode("utf-8"),
    )

    # Get user input information
    messagepayload = json.loads(inputqueue.get_body().decode("utf-8"))
    machine = messagepayload.get("machine", "")
    outcome = messagepayload.get("outcome", "Throughput (BPM)")
    new_values = messagepayload.get("new_values", 100)
    timestamp = messagepayload.get("datetime", datetime.utcnow().isoformat())
    mode = messagepayload.get("mode", "predict")
    correlation_id = messagepayload["CorrelationId"]

    # Make up some new KPI outcomes
    original = 251
    predicted = 257

    response_data = {}
    if mode == "predict":
        # If new_value is a percent, extract and adjust original value
        # otherwise, just make sure it is converted to a float
        tag_name, new_value = new_values.split("=")
        if isinstance(new_value, str) and new_value.endswith("%"):
            new_value = float(new_value[:-1]) / 100 * 100
        else:
            new_value = float(new_values)

        # Create the response dictionary
        response_data = {
            "timestamp": timestamp,
            "tag_name": tag_name,
            "new_value": new_value,
            "outcome": outcome,
            "original": original,
            "predicted": predicted,
        }
    elif mode == "anomaly":
        # Create the response dictionary for anomaly detection
        response_data = {
            "timestamp": timestamp,
            "tag_name": "Pressure_PV",
            "original": 100,
            "anomaly": 108,
        }

    result_message = {
        "Value": str(response_data),
        "CorrelationId": correlation_id,
    }
    outputqueue.set(json.dumps(result_message).encode("utf-8"))

    logging.info(
        "Sent message to queue: nameoutputqueue with message %s", result_message
    )
