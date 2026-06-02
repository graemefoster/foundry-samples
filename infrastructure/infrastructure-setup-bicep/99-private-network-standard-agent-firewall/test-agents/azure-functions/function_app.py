import azure.functions as func
import json
import logging

app = func.FunctionApp()

# Name of the queues to get and send the function call messages
input_queue_name = "inputqueuetest"
output_queue_name = "outputqueuetest"

# Function to get the weather
@app.function_name(name="GetWeather")
@app.queue_output(arg_name="outputQueueItem",  queue_name=output_queue_name, connection="STORAGE_CONNECTION")
@app.queue_trigger(arg_name="msg", queue_name=input_queue_name, connection="STORAGE_CONNECTION") 
def process_queue_message(msg: func.QueueMessage,  outputQueueItem: func.Out[str]) -> None:
    logging.info('Python queue trigger function processed a queue item')

    messagepayload = json.loads(msg.get_body().decode('utf-8'))
    location = messagepayload['location']
    correlation_id = messagepayload['CorrelationId']

    # Send message to queue. Sends a mock message for the weather
    result_message = {
        'Value': 'Weather is 25 degrees Celsius and cloudy in ' + location,
        'CorrelationId': correlation_id
    }
    outputQueueItem.set(json.dumps(result_message).encode('utf-8'))

    logging.info(f"Sent message to queue: {output_queue_name} with message {result_message}")
    
    
# {
#     "location": "Perth",
#     "CorrelationId": "1234"
# }
