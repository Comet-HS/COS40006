#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import os
import queue
from threading import Thread
import logging
import json

import aiko_services as aiko

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFINITION_PATHNAME = "../pipelines/llm_pipeline.json"
PIPELINE_NAME = "p_llm"
STREAM_ID = "*"

app = Flask(__name__, static_folder='static')

reminders = []

def create_pipeline(definition_pathname, name):
    if not os.path.exists(definition_pathname):
        raise SystemExit(f"Error: PipelineDefinition not found: {definition_pathname}")

    pipeline_definition = aiko.PipelineImpl.parse_pipeline_definition(definition_pathname)

    response_queue = queue.Queue()
    stream_id = "*"

    pipeline = aiko.PipelineImpl.create_pipeline(
        definition_pathname, pipeline_definition, name, stream_id,
        stream_parameters=(), frame_id=0, frame_data=None, grace_time=3600,
        queue_response=response_queue)
    thread = Thread(target=pipeline.run)
    thread.daemon = True
    thread.start()
    return pipeline, response_queue

def process_request(pipeline, response_queue, request):
    try:
        stream = {"stream_id": STREAM_ID}
        pipeline.process_frame(stream, request)
        result = response_queue.get()[1]
        logger.info(f"Raw result from pipeline: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {"error": str(e), "response": "I apologize, but I encountered an error processing your request. Could you please try again?"}

def add_reminder(reminder_details):
    global reminders
    formatted_reminder = f"{reminder_details['date']} {reminder_details['time']}: {reminder_details['details']}"
    reminders.append(formatted_reminder)
    logger.info(f"Added reminder: {formatted_reminder}")

@app.route('/')
def index():
    return render_template('index.html', reminders=reminders)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    logger.info(f"Received user input: {user_input}")
    if user_input:
        pipeline, response_queue = app.config["pipeline"]
        result = process_request(pipeline, response_queue, {"text": user_input})
        logger.info(f"Sending response: {result}")
        return jsonify(result)
    logger.warning("No input provided")
    return jsonify({"error": "No input provided"}), 400

if __name__ == '__main__':
    pipeline_config = create_pipeline(DEFINITION_PATHNAME, PIPELINE_NAME)
    app.config["pipeline"] = pipeline_config
    app.run(debug=True)