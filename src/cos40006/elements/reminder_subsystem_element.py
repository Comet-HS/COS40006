import aiko_services as aiko
import sqlite3
from datetime import datetime
import threading
import time
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Global list to store notifications
notifications = []

class ReminderSubsystemElement(aiko.PipelineElement):
    def __init__(self, context):
        if context:
            context.set_protocol("reminder:0")
            context.get_implementation("PipelineElement").__init__(self, context)
        else:
            logger.info("Running without context (standalone mode)")

        self.db_path = os.path.join(os.path.dirname(__file__), '../../reminder_data.db')
        logger.info(f"Using database at: {os.path.abspath(self.db_path)}")

        self.create_reminders_table()

        self.thread = threading.Thread(target=self.reminder_check_loop, daemon=True)
        self.thread.start()

    def create_reminders_table(self):
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

    def process_frame(self, stream, frame=None, **kwargs):
        if frame is None:
            frame = kwargs

        if not isinstance(frame, dict):
            logger.error("Frame data must be a dictionary!")
            return aiko.StreamEvent.ERROR, {}

        reminder_text = frame.get("reminder_text")
        reminder_time = frame.get("reminder_time")

        if not reminder_text or not reminder_time:
            logger.warning("Reminder text or time is missing.")
            return aiko.StreamEvent.OKAY, frame

        self.save_reminder_to_db(reminder_text, reminder_time)

        logger.info(f"Reminder set: {reminder_text} at {reminder_time}")
        return aiko.StreamEvent.OKAY, {"processed_reminder": f"Reminder set: {reminder_text} at {reminder_time}"}

    def save_reminder_to_db(self, text, time):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO reminders (text, time, notified) VALUES (?, ?, 0)
            ''', (text, time))

            connection.commit()
            connection.close()

            logger.info(f"Saved reminder: {text} at {time}")
        except Exception as e:
            logger.error(f"Error saving reminder to DB: {str(e)}")

    def reminder_check_loop(self):
        logger.info("Starting the reminder notification check loop...")
        while True:
            logger.debug(f"Checking reminders at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            self.check_and_notify()
            time.sleep(30)

    def check_and_notify(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        cursor.execute('''
            SELECT id, text FROM reminders WHERE time <= ? AND notified = 0
        ''', (now,))

        due_reminders = cursor.fetchall()

        for reminder_id, text in due_reminders:
            self.notify_user(text)
            self.update_notification_status(reminder_id)

        connection.commit()
        connection.close()

    def notify_user(self, reminder_text):
        logger.info(f"Reminder Notification: {reminder_text}")
        global notifications
        notifications.append(f"Reminder: {reminder_text}")

    def update_notification_status(self, reminder_id):
        connection = sqlite3.connect(self.db_path)
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
    logger.info("ReminderSubsystemElement loaded successfully.")
