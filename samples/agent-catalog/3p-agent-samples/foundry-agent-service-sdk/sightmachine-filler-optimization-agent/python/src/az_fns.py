import os
import json
import logging
from datetime import datetime
import pytz
import random

import pandas as pd
import azure.functions as func

###
### Set of azure functions for user with the Filler AI Agent
### This is a set of stub functions for proof of concept
### For full production code that accesses Sight Machine,
### Please contact us via https://sightmachine.com/contact/
###


def get_demo_data(timestamp):
    # This function is a stub for demo purposes
    # In normal operation, this would be a call to the Sight Machine API
    # Instead we will pull data from a CSV file, fix the date so you can answer "now" questions and return just the most recent matching timestamp
    # For a full operation, contact Sight Machine as described in the README

    if not timestamp:
        # If no timestamp is provided, use the current time
        timestamp = datetime.now()

    if isinstance(timestamp, str):
        # Convert the string to a datetime object
        timestamp = pd.to_datetime(timestamp)

    # Round timestamp to the neareset minute
    timestamp = timestamp.replace(
        second=0, microsecond=0
    )  # Round to the nearest minute

    ### We are going to hardcode the timezone for demo purposes
    # This will guarantee that there is data to reply
    eastern = pytz.timezone("US/Eastern")
    timestamp = eastern.localize(timestamp)

    # Get example data from the CSV file
    file_path = os.path.join(
        os.path.dirname(__file__), "..", "sample_data", "example_data.csv"
    )

    df = pd.read_csv(file_path)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Make the fake data timestamp match the one in the message
    date_part = timestamp.date()
    df["Timestamp"] = df["Timestamp"].apply(
        lambda x: datetime.combine(date_part, x.to_pydatetime().time())
    )
    df["Timestamp"] = df["Timestamp"].dt.tz_localize(eastern)

    # For demo purposes, just return the matching timestamp
    df = df[df["Timestamp"] == timestamp]

    return df


def data_queue_trigger(
    inputqueue: func.QueueMessage, outputqueue: func.Out[str]
) -> None:

    # This is a stub for demo purposes
    # The demo CSV file only has data for one day for a fixed machine
    # In normal operation, this would be a call to the Sight Machine API
    # For a full operation, contact Sight Machine as described in the README

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

    # Note that the demo data only had Pressure and Temperature
    df = get_demo_data(timestamp)
    column_names = column_names.split(",")

    # Convert df["Timestamp"] to string for reporting
    df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df = df.set_index("Timestamp")
    data = df[column_names].to_dict()

    # Send message to queue. Sends a mock messaage for the data
    result_message = {
        "Value": f"Data for {machine_name}: {data}",
        "CorrelationId": correlation_id,
    }
    outputqueue.set(json.dumps(result_message).encode("utf-8"))

    logging.info(
        "Sent message to queue: nameoutputqueue with message %s", result_message
    )


def name_queue_trigger(
    inputqueue: func.QueueMessage, outputqueue: func.Out[str]
) -> None:
    # This is a stub for demo purposes
    # In normal operation, this would be a call to the Sight Machine Factory Namespace Manager
    # For a full operation, contact Sight Machine as described in the README

    logging.info(
        "Python Queue trigger processed a message: %s",
        inputqueue.get_body().decode("utf-8"),
    )

    # Get user input information
    messagepayload = json.loads(inputqueue.get_body().decode("utf-8"))
    column_names = messagepayload.get("columns", "Throughput")
    machine_names = messagepayload.get("machines", "Line 1 Filler")
    correlation_id = messagepayload["CorrelationId"]

    # For demo purposes, we only know about Pressure, Temperature and Throughput
    mapped_names = {}
    for col in column_names.split(","):
        if "PRESSURE" in col.upper():
            mapped_names[col] = "Pressure_PV"
        elif "TEMPERATURE" in col.upper():
            mapped_names[col] = "Temperature_PV"
        elif "THROUGHPUT" in col.upper():
            mapped_names[col] = "Throughput (BPM)"

    # For demo purposes, we only know about Line 1 Filler
    machine_names = {mach: "L1_Filler" for mach in machine_names.split(",")}

    renamed_pairs = mapped_names.copy()
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
    # This is a stub for demo purposes
    # In normal operation, this would be a call to the Sight Machine Auto ML API
    # For a full operation, contact Sight Machine as described in the README

    logging.info(
        "Python Queue trigger processed a message: %s",
        inputqueue.get_body().decode("utf-8"),
    )

    # Get user input information
    messagepayload = json.loads(inputqueue.get_body().decode("utf-8"))
    machine = messagepayload.get("machine", "L1_Filler")
    outcome = messagepayload.get("outcome", "Throughput (BPM)")
    new_values = messagepayload.get("new_values", 100)
    timestamp = messagepayload.get("datetime", datetime.utcnow().isoformat())
    mode = messagepayload.get("mode", "predict")
    correlation_id = messagepayload["CorrelationId"]

    df = get_demo_data(timestamp)
    # Force the coutcome to Throughput for demo stub
    outcome = "Throughput (BPM)"

    response_data = {}
    if mode == "predict":
        # Normally we'd make a call the SM Auto ML.
        # For demo, assume the percent change in throughput is the percent change in the input predictor

        # If new_value is a percent, extract and adjust original value
        # otherwise, just make sure it is converted to a float

        # new values will be of the form Variable=Value or Variable=Percent
        tag_name, new_value = new_values.split("=")
        old_value = df[tag_name].iloc[0]

        if isinstance(new_value, str) and new_value.endswith("%"):
            new_value = float(new_value[:-1]) / 100 * old_value
        else:
            new_value = float(new_values)

        # Since we are hacking a prediction, we need to find the % change
        ratio = new_value / old_value

        # Simulate a prediction using the percent change in the input tag
        original = df[outcome].iloc[0]
        predicted = original * ratio
        predicted = round(predicted, 2)

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
        # Make a fake anomaly on the Pressure
        # Just assume the anomaly is right now, and simulate a random value
        original = df["Pressure_PV"].iloc[0]
        anomaly = original * random.uniform(0.8, 1.2)  # Simulate an anomaly
        anomaly = round(anomaly, 2)

        # Create the response dictionary for anomaly detection
        response_data = {
            "timestamp": timestamp,
            "tag_name": "Pressure_PV",
            "original": original,
            "anomaly": anomaly,
        }

    result_message = {
        "Value": str(response_data),
        "CorrelationId": correlation_id,
    }
    outputqueue.set(json.dumps(result_message).encode("utf-8"))

    logging.info(
        "Sent message to queue: nameoutputqueue with message %s", result_message
    )
