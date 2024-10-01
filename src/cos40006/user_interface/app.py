#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import os
import queue
from threading import Thread
import logging

import aiko_services as aiko

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DEFINITION_PATHNAME = "../pipelines/llm_pipeline.json"
PIPELINE_NAME = "p_llm"
STREAM_ID = "*"

app = Flask(__name__)

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
        response = response_queue.get()[1]
    except Exception as e:
        response = {"error": str(e)}
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')
    if user_input:
        pipeline, response_queue = app.config["pipeline"]
        result = process_request(pipeline, response_queue, {"text": user_input})
        return jsonify(result)
    return jsonify({"error": "No input provided"}), 400

if __name__ == '__main__':
    pipeline_config = create_pipeline(DEFINITION_PATHNAME, PIPELINE_NAME)
    app.config["pipeline"] = pipeline_config
    app.run(debug=True)