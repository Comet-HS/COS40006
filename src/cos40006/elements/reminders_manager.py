import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import requests  # Assuming this will be used to make API calls to Aiko's TTS system

class ReminderManager:
    def __init__(self):
        self.reminders: List[Dict[str, Any]] = []
        self.logger = logging.getLogger("ReminderManager")
        self.load_reminders()

    def add_reminder(self, text: str, reminder_time: str) -> None:
        """
        Add a new reminder.
        """
        reminder = {
            'text': text,
            'time': reminder_time,
            'notified': False
        }
        self.reminders.append(reminder)
        self.logger.info(f"Added reminder: {text} at {reminder_time}")

    def check_reminders(self) -> List[Dict[str, Any]]:
        """
        Check for due reminders and return those that are due.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        due_reminders = []
        for reminder in self.reminders:
            if reminder['time'] <= now and not reminder['notified']:
                reminder['notified'] = True
                self.logger.info(f"Reminder due: {reminder['text']}")
                due_reminders.append(reminder)
                self.notify_user(reminder['text'])  # Notify user when the reminder is due
        return due_reminders

    def get_reminders(self) -> List[Dict[str, Any]]:
        """
        Retrieve the list of reminders.
        """
        return self.reminders

    def save_reminders(self) -> None:
        """
        Save reminders to a JSON file.
        """
        with open('reminders.json', 'w') as f:
            json.dump(self.reminders, f)
        self.logger.info("Reminders saved to file.")

    def load_reminders(self) -> None:
        """
        Load reminders from a JSON file.
        """
        try:
            with open('reminders.json', 'r') as f:
                self.reminders = json.load(f)
            self.logger.info("Reminders loaded from file.")
        except FileNotFoundError:
            self.reminders = []
            self.logger.info("No previous reminders found. Starting fresh.")

    def notify_user(self, message: str) -> None:
        """
        Send a notification for a reminder.
        """
        self.logger.info(f"Notifying user: {message}")
