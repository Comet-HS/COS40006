import aiko_services as aiko
import sqlite3
from datetime import datetime
from typing import Tuple, Any
import threading
import time
import os

# Global list to store notifications
notifications = []  # This will be accessed by the Flask app to send notifications to the front-end

class ReminderSubsystemElement(aiko.PipelineElement):
    def __init__(self, context):
        if context:
            context.set_protocol("reminder:0")
            context.get_implementation("PipelineElement").__init__(self, context)
        else:
            print("Running without context (standalone mode)")

        # Use the correct path for the database
        self.db_path = os.path.join(os.path.dirname(__file__), '../reminder_data.db')

        # Create the reminders table if it doesn't exist
        self.create_reminders_table()

        # Start the reminder checking thread
        self.thread = threading.Thread(target=self.reminder_check_loop, daemon=True)
        self.thread.start()

    def create_reminders_table(self):
        """Creates the reminders table in the database if it does not exist."""
        connection = sqlite3.connect(self.db_path)  # Use updated path
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

    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        """Processes a frame to set a reminder in the system."""
        if frame is None:
            frame = kwargs

        # Ensure the frame is a dictionary
        if not isinstance(frame, dict):
            self.logger.error("Frame data must be a dictionary!")
            return aiko.StreamEvent.ERROR, {}

        reminder_text = frame.get("reminder_text")
        reminder_time = frame.get("reminder_time")

        if not reminder_text or not reminder_time:
            print("Reminder text or time is missing.")
            return aiko.StreamEvent.OKAY, frame

        # Store the reminder in the database
        self.save_reminder_to_db(reminder_text, reminder_time)

        # Log and return the processed result
        print(f"Reminder set: {reminder_text} at {reminder_time}")
        return aiko.StreamEvent.OKAY, {"processed_reminder": f"Reminder set: {reminder_text} at {reminder_time}"}

    def save_reminder_to_db(self, text, time):
        """Saves a reminder to the database."""
        connection = sqlite3.connect(self.db_path)  # Use updated path
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO reminders (text, time, notified) VALUES (?, ?, 0)
        ''', (text, time))

        connection.commit()
        connection.close()

        print(f"Saved reminder: {text} at {time}")

    def reminder_check_loop(self):
    """Continuously checks for reminders to notify every 30 seconds."""
    print("Starting the reminder notification check loop...")
    while True:
        print(f"Checking reminders at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.check_and_notify()
        time.sleep(30)  # Adjust the sleep time if needed

    def check_and_notify(self):
        """Checks the database for due reminders and sends notifications."""
        connection = sqlite3.connect(self.db_path)  # Use updated path
        cursor = connection.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Select all reminders that are due and not notified
        cursor.execute('''
            SELECT id, text FROM reminders WHERE time <= ? AND notified = 0
        ''', (now,))

        due_reminders = cursor.fetchall()

        # Notify and mark each reminder as notified
        for reminder_id, text in due_reminders:
            self.notify_user(text)
            self.update_notification_status(reminder_id)

        connection.commit()
        connection.close()

    def notify_user(self, reminder_text):
        """Simulates sending a notification to the user."""
        print(f"Reminder Notification: {reminder_text}")

        # Add the notification to the global notifications list for the UI
        global notifications
        notifications.append(f"Reminder: {reminder_text}")

    def update_notification_status(self, reminder_id):
        """Marks a reminder as notified in the database."""
        connection = sqlite3.connect(self.db_path)  # Use updated path
        cursor = connection.cursor()

        cursor.execute('''
            UPDATE reminders SET notified = 1 WHERE id = ?
        ''', (reminder_id,))

        connection.commit()
        connection.close()

    # Implementing required abstract methods with basic functionality
    def add_message_handler(self, *args, **kwargs): pass
    def add_tags(self, *args, **kwargs): pass
    def add_tags_string(self, *args, **kwargs): pass
    def create_frame(self, *args, **kwargs): pass
    def create_frames(self, *args, **kwargs): pass
    def get_parameter(self, *args, **kwargs): pass
    def get_stream(self, *args, **kwargs): pass
    def get_stream_parameters(self, *args, **kwargs): pass
    def get_tags_string(self, *args, **kwargs): pass
    def my_id(self, *args, **kwargs): pass
    def registrar_handler_call(self, *args, **kwargs): pass
    def remove_message_handler(self, *args, **kwargs): pass
    def run(self, *args, **kwargs): pass
    def set_registrar_handler(self, *args, **kwargs): pass
    def start_stream(self, *args, **kwargs): pass
    def stop(self, *args, **kwargs): pass
    def stop_stream(self, *args, **kwargs): pass

if __name__ == "__main__":
    context = None  # Bypass context for standalone testing
    element = ReminderSubsystemElement(context)
    print("ReminderSubsystemElement loaded successfully.")
