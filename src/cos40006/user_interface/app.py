import threading
import time
from flask import Flask, render_template, request, jsonify
import sys
import os
import queue
import logging
import json
import aiko_services as aiko
import speech_recognition as sr

# Ensure the elements module path is accessible
elements_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'elements'))
sys.path.append(elements_path)

from speech_to_text_element import SpeechToTextElement

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFINITION_PATHNAME = "../pipelines/llm_pipeline.json"
PIPELINE_NAME = "p_llm"
STREAM_ID = "*"

app = Flask(__name__, static_folder='static')
reminders = []

# Create an instance of the SpeechToTextElement
stt_element = SpeechToTextElement(None)
response_queue = queue.Queue()

def create_pipeline(definition_pathname, name):
    if not os.path.exists(definition_pathname):
        raise SystemExit(f"Error: PipelineDefinition not found: {definition_pathname}")

    pipeline_definition = aiko.PipelineImpl.parse_pipeline_definition(definition_pathname)
    pipeline = aiko.PipelineImpl.create_pipeline(
        definition_pathname, pipeline_definition, name, STREAM_ID,
        stream_parameters=(), frame_id=0, frame_data=None, grace_time=3600
    )
    thread = threading.Thread(target=pipeline.run)
    thread.daemon = True
    thread.start()
    return pipeline, response_queue

def process_request(pipeline, response_queue, request):
    try:
        stream = {"stream_id": STREAM_ID}
        pipeline.process_frame(stream, request)
        response = response_queue.get()[1]
        if isinstance(response, dict) and 'response' in response:
            parsed_response = json.loads(response['response'])
        else:
            raise ValueError("Unexpected response format")
        
        if parsed_response.get('reminder_details'):
            add_reminder(parsed_response['reminder_details'])
        
        return parsed_response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {"error": str(e), "response": "I encountered an error processing your request. Please try again."}

def add_reminder(reminder_details):
    global reminders
    formatted_reminder = f"{reminder_details['date']} {reminder_details['time']}: {reminder_details['details']}"
    reminders.append(formatted_reminder)
    logger.info(f"Added reminder: {formatted_reminder}")

@app.route('/')
def index():
    return render_template('index.html', reminders=reminders)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    try:
        # Convert the audio file into a format suitable for processing
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)

        # Use the recognizer to transcribe the audio
        recognized_text = recognizer.recognize_google(audio)
        return jsonify({'recognized_text': recognized_text})
    except sr.UnknownValueError:
        return jsonify({'recognized_text': 'Could not understand the audio'}), 200
    except sr.RequestError as e:
        return jsonify({'error': f'Error with speech recognition service: {e}'}), 500
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return jsonify({'error': 'Audio file could not be read as PCM WAV, AIFF/AIFF-C, or Native FLAC; check if file is corrupted or in another format'}), 500

if __name__ == '__main__':
    pipeline_config = create_pipeline(DEFINITION_PATHNAME, PIPELINE_NAME)
    app.config["pipeline"] = pipeline_config

    # Run the Flask app
    app.run(debug=True)
