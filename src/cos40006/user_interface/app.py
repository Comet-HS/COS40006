#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import os
import queue
from threading import Thread
import logging
import json
import sqlite3
from datetime import datetime
import time
import threading  # Importing threading for the reminder loop
import speech_recognition as sr
import io
import base64

import aiko_services as aiko
from cos40006.database_setup import get_db_path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFINITION_PATHNAME = "../pipelines/llm_pipeline.json"
PIPELINE_NAME = "p_llm"
STREAM_ID = "*"

app = Flask(__name__, static_folder='static')

reminders = []
notifications = []  # Create a global notifications list


# Reminder Subsystem Element class for handling reminders and notifications
class ReminderSubsystemElement:
    def __init__(self):
        self.db_path = get_db_path()
        self.create_reminders_table()
        self.thread = threading.Thread(target=self.reminder_check_loop, daemon=True)
        self.thread.start()

    def create_reminders_table(self):
        """Creates the reminders table in the database if it does not exist."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                time TEXT NOT NULL,
                notified INTEGER DEFAULT 0
            )
        ''')

        connection.commit()
        connection.close()

    def save_reminder_to_db(self, text, time):
        """Saves a reminder to the database."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO reminders (text, time, notified) VALUES (?, ?, 0)
        ''', (text, time))

        connection.commit()
        connection.close()

        print(f"Saved reminder: {text} at {time}")

    def reminder_check_loop(self):
        """Continuously checks for reminders to notify every 10 seconds."""
        print("Starting the reminder notification check loop...")
        while True:
            self.check_and_notify()
            time.sleep(10)  # Wait 10 seconds before checking again

    def check_and_notify(self):
        """Checks the database for due reminders and sends notifications."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"Current time: {now}")  # Debugging log

        # Select all reminders that are due and not notified
        cursor.execute('''
            SELECT id, text, time FROM reminders WHERE notified = 0
        ''')

        due_reminders = cursor.fetchall()
        for reminder_id, text, reminder_time in due_reminders:
            print(f"Checking reminder: {text}, due at: {reminder_time}")  # Debugging log
            if reminder_time <= now:
                print(f"Reminder {text} is due now!")  # Debugging log
                self.notify_user(text)
                self.update_notification_status(reminder_id)

        connection.commit()
        connection.close()

    def notify_user(self, reminder_text):
        """Simulates sending a notification to the user."""
        global notifications  # Reference the global notifications list
        print(f"Reminder Notification: {reminder_text}")
        notifications.append(f"Reminder: {reminder_text}")  # Add the notification to the list

    def update_notification_status(self, reminder_id):
        """Marks a reminder as notified in the database."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute('''
            UPDATE reminders SET notified = 1 WHERE id = ?
        ''', (reminder_id,))

        connection.commit()
        connection.close()


# Create and start the ReminderSubsystemElement
reminder_subsystem = ReminderSubsystemElement()


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
        if isinstance(response, dict) and 'response' in response:
            parsed_response = json.loads(response['response'])
        else:
            raise ValueError("Unexpected response format")

        # Check if there's a reminder to add
        if parsed_response.get('reminder_details'):
            add_reminder(parsed_response['reminder_details'])

        return parsed_response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {"error": str(e), "response": "I apologize, but I encountered an error processing your request. Could you please try again?"}


def add_reminder(reminder_details):
    global reminders
    formatted_reminder = f"{reminder_details['date']} {reminder_details['time']}: {reminder_details['details']}"
    reminders.append(formatted_reminder)
    logger.info(f"Added reminder: {formatted_reminder}")

    # Save the reminder to the database
    reminder_subsystem.save_reminder_to_db(reminder_details['details'], f"{reminder_details['date']} {reminder_details['time']}")


@app.route('/')
def index():
    connection = sqlite3.connect(reminder_subsystem.db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT id, text, time FROM reminders ORDER BY time')
    reminders = [f"{row[0]}: {row[2]} - {row[1]}" for row in cursor.fetchall()]
    connection.close()
    return render_template('index.html', reminders=reminders)


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')
    speak_response = request.form.get('speak_response') == 'true'
    if user_input:
        pipeline, response_queue = app.config["pipeline"]
        result = process_request(pipeline, response_queue, {"text": user_input})

        emotion_details = None
        if result.get("emotion_details"):
            emotion_details = result["emotion_details"]

        return jsonify({
            "response": result,
            "reminders": reminders,
            "emotion_details": emotion_details,
            "speak_response": speak_response
        })
    return jsonify({"error": "No input provided"}), 400


@app.route('/add_reminder', methods=['POST'])
def add_reminder_from_ui():
    reminder_text = request.form.get('reminder_text')
    reminder_time = request.form.get('reminder_time')

    # Debugging log
    print(f"Received reminder from UI: {reminder_text} at {reminder_time}")

    if reminder_text and reminder_time:
        try:
            # Save the reminder to the database
            reminder_subsystem.save_reminder_to_db(reminder_text, reminder_time)
            return jsonify({"status": "Reminder added successfully"})
        except Exception as e:
            logger.error(f"Error while saving reminder: {str(e)}")
            return jsonify({"status": "Failed to add reminder", "error": str(e)}), 500
    else:
        return jsonify({"status": "Failed to add reminder due to missing data"}), 400


@app.route('/get_notifications', methods=['GET'])
def get_notifications():
    global notifications
    new_notifications = notifications.copy()  # Copy current notifications
    notifications.clear()  # Clear the notifications list after sending them to the front-end
    return jsonify({"notifications": new_notifications})


@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Get the base64 encoded audio data from the request
        audio_data_base64 = request.json['audio']
        
        # Decode the base64 audio data
        audio_data = base64.b64decode(audio_data_base64.split(',')[1])
        
        # Create a speech recognition object
        recognizer = sr.Recognizer()
        
        # Convert the audio data to an AudioFile
        with io.BytesIO(audio_data) as audio_file:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
        
        # Perform speech recognition
        text = recognizer.recognize_google(audio)
        
        # Process the recognized text through the pipeline
        pipeline, response_queue = app.config["pipeline"]
        result = process_request(pipeline, response_queue, {"text": text})
        
        # Extract emotion details from the result if present
        emotion_details = None
        if result.get("emotion_details"):
            emotion_details = result["emotion_details"]
        
        return jsonify({
            "response": result,
            "reminders": reminders,
            "emotion_details": emotion_details,
            "transcribed_text": text,
            "speak_response": True  # Always speak responses to voice input
        })
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}", exc_info=True)
        return jsonify({"error": str(e), "response": "I apologize, but I encountered an error processing your audio. Could you please try again?"}), 400


@app.route('/delete_reminder', methods=['POST'])
def delete_reminder():
    reminder_id = request.form.get('reminder_id')
    if reminder_id:
        try:
            connection = sqlite3.connect(get_db_path())
            cursor = connection.cursor()
            
            cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
            connection.commit()
            
            # Fetch updated reminders
            cursor.execute('SELECT id, text, time FROM reminders ORDER BY time')
            reminders = [f"{row[0]}: {row[2]} - {row[1]}" for row in cursor.fetchall()]
            
            connection.close()
            
            return jsonify({"status": "success", "reminders": reminders})
        except Exception as e:
            logger.error(f"Error deleting reminder: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "No reminder ID provided"}), 400


if __name__ == '__main__':
    # Create the pipeline
    pipeline_config = create_pipeline(DEFINITION_PATHNAME, PIPELINE_NAME)
    app.config["pipeline"] = pipeline_config

    # Install required packages
    os.system('pip install SpeechRecognition')

    # Start the Flask app
    app.run(debug=True)
