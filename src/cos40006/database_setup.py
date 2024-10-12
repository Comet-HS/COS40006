import os
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db_path():
    return os.path.join(os.path.dirname(__file__), 'reminder_data.db')

def initialize_database():
    db_path = get_db_path()
    logger.info(f"Using database at: {os.path.abspath(db_path)}")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create the reminders table with notification status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            time TEXT NOT NULL,
            notified INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Create a notifications table to track notifications
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder_id INTEGER,
            notification_time TEXT NOT NULL,
            message TEXT NOT NULL,
            FOREIGN KEY (reminder_id) REFERENCES reminders(id) ON DELETE CASCADE
        )
    ''')

    # Create the emotions table to store detected emotions related to a reminder
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder_id INTEGER,
            detected_emotion TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reminder_id) REFERENCES reminders(id) ON DELETE CASCADE
        )
    ''')

    connection.commit()
    connection.close()
    logger.info("Database initialized with reminders, notifications, and emotions tables.")

def save_reminder_to_db(text, time):
    """Saves a reminder to the SQLite database."""
    try:
        logger.info(f"Attempting to save reminder: {text} at {time}")
        
        connection = sqlite3.connect(get_db_path())
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO reminders (text, time, notified) VALUES (?, ?, 0)
        ''', (text, time))

        connection.commit()
        connection.close()
        logger.info(f"Reminder saved: {text} at {time}")
    except Exception as e:
        logger.error(f"Error saving reminder to DB: {str(e)}")

if __name__ == '__main__':
    initialize_database()
    logger.info("Database initialized.")

    # Example: Saving a reminder (You can remove or modify this part for testing purposes)
    save_reminder_to_db("Call mom", "2024-10-12 15:00")
