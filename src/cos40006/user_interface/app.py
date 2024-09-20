#!/usr/bin/env python3

# TODO ...
# pip install -e .  # at the project top-level
# cd user_interface
#
# export PYTHONPATH=../sample  # TODO: Temporary until pyproject.toml fixed
# # AIKO_LOG_LEVEL=DEBUG  # optional, default is INFO
# ./cli_sync.py ../pipeline_ui.json

from flask import Flask, render_template, request, redirect, url_for
import os
import queue
from threading import Thread

import aiko_services as aiko

DEFINITION_PATHNAME = "../pipelines/pipeline_example.json"
# DEFINITION_PATHNAME = "../sample/pipeline_llm.json"
PIPELINE_NAME = "p_reminder"
STREAM_ID = "*"
TEST_MODE = False

app = Flask(__name__)
def create_pipeline(definition_pathname, name):
    if not os.path.exists(definition_pathname):
        raise SystemExit(
            f"Error: PipelineDefinition not found: {definition_pathname}")

    pipeline_definition = aiko.PipelineImpl.parse_pipeline_definition(
        definition_pathname)

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
        response = response_queue.get()[1]["reversed_text"]
    except ValueError:
        response = "Input must be an integer"
    return response

# Sample data
# Replace with a database (suggestion: sqlite)
reminders = [
    "Monday 9 am: Take vitamin tablets",
    "Tuesday 12 noon: See doctor"
]

# initialization
@app.route('/')
def index():
    return render_template('index.html', reminders=reminders)

# route to add new reminder. Currently only updating a list!!
@app.route('/new_reminder', methods=['POST'])
def new_reminder():
    new_task = request.form.get('new_reminder')
    if new_task:
        pipeline, response_queue = app.config["pipeline"]
        task_request = {"text": new_task}
        task_response = process_request(pipeline, response_queue, task_request)

        reminders.append(task_response)
    return redirect(url_for('index'))


# A Placeholder form to communicate with an LLM
# Currently only prints the mressage received into the terminal
@app.route('/ask_assistant', methods=['POST'])
def ask_assistant():
    question = request.form.get('assistant_question')
    print(f"Assistant question received: {question}")
    return redirect(url_for('index'))

if TEST_MODE:
    pipeline, response_queue = create_pipeline(
        DEFINITION_PATHNAME, PIPELINE_NAME)

    request = {"text": "hello"}
    response = process_request(pipeline, response_queue, request)
    raise SystemExit(response)

if __name__ == '__main__':
    pipeline_config = create_pipeline(DEFINITION_PATHNAME, PIPELINE_NAME)
    app.config["pipeline"] = pipeline_config
    app.run(debug=True)