from flask import Flask, render_template, request, redirect, url_for
import os
import queue
from threading import Thread
from datetime import datetime

import aiko_services as aiko

app = Flask(__name__)

# Initialize with two sample reminders
reminders = [
    "Monday 9 am: Take vitamin tablets",
    "Tuesday 12 noon: See doctor"
]



@app.route('/')
def index():
    return render_template('index.html', reminders=reminders)

@app.route('/new_reminder', methods=['POST'])
def new_reminder():
    new_reminder_text = request.form['new_reminder']
    reminders.append(new_reminder_text)
    return redirect(url_for('index'))

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    text = request.form['text']
    time = request.form['time']
    
    if text and time:
        reminder_time = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        formatted_reminder = f"{reminder_time.strftime('%A %I:%M %p')}: {text}"
        reminders.append(formatted_reminder)

        # Trigger Aiko to process reminder (example of integration)
        process_reminder_with_aiko(text, reminder_time)
    
    return redirect(url_for('index'))

def process_reminder_with_aiko(text, reminder_time):
    # This is where the reminder can be processed using Aiko services
    # integrate Aiko pipeline or elements to process this reminder.
    # Example:
    print(f"Processing reminder: {text} at {reminder_time}")
    #need to send this reminder to aiko_services if integrated with your pipeline

@app.route('/ask_assistant', methods=['POST'])
def ask_assistant():
    assistant_question = request.form['assistant_question']
    assistant_response = assistant_question[::-1]  # Reverse the input text for now
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
