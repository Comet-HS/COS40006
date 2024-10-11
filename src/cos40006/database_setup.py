import sqlite3

def initialize_database():
    # Use the correct path to the database file
    db_path = os.path.join(os.path.dirname(__file__), '../reminder_data.db')
    print("Using database at:", os.path.abspath(db_path))  # Print the absolute path

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()


    # Create the reminders table with notification status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            time TEXT NOT NULL,
            notified BOOLEAN NOT NULL DEFAULT 0  -- Notification status (0 = not notified, 1 = notified)
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
    print("Database initialized with reminders, notifications, and emotions tables.")

def save_reminder_to_db(text, time):
    """Saves a reminder to the SQLite database."""
    try:
        print(f"Attempting to save reminder: {text} at {time}")  # Debugging log
        
        connection = sqlite3.connect('project_data.db')
        cursor = connection.cursor()

        # Insert the reminder into the database as it is, assuming the time format is correct
        cursor.execute('''
            INSERT INTO reminders (text, time, notified) VALUES (?, ?, 0)
        ''', (text, time))

        connection.commit()
        connection.close()
        print(f"Reminder saved: {text} at {time}")  # Debugging log
    except Exception as e:
        logger.error(f"Error saving reminder to DB: {str(e)}")
        print(f"Error: {str(e)}")  # Extra log for debugging

if __name__ == '__main__':
    initialize_database()
    print("Database initialized.")

    # Example: Saving a reminder (You can remove or modify this part for testing purposes)
    save_reminder_to_db("Call mom", "2024-10-12 15:00")
