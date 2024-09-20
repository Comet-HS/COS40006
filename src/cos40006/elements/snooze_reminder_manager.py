import aiko_services as aiko
from datetime import datetime, timedelta
import logging
import json

class SnoozeReminderManager(aiko.PipelineElement):
    def __init__(self, context):
        # Initialize the snooze reminder manager and set protocol
        if context:
            context.set_protocol("snooze_reminder:0")
            context.get_implementation("PipelineElement").__init__(self, context)

        self.reminders = []
        self.logger = logging.getLogger("SnoozeReminderManager")
        self.load_reminders()

    def add_reminder(self, text: str, reminder_time: str) -> None:
        # Add a new reminder
        reminder = {'text': text, 'time': reminder_time, 'notified': False}
        self.reminders.append(reminder)
        self.logger.info(f"Added reminder: {text} at {reminder_time}")
        print(f"Reminder added: {reminder}")  # Print to verify the reminder added
        self.save_reminders()

    def snooze_reminder(self, reminder: dict, snooze_minutes: int) -> None:
        # Snooze the reminder by a given number of minutes
        reminder_time = datetime.strptime(reminder['time'], "%Y-%m-%d %H:%M")
        snoozed_time = reminder_time + timedelta(minutes=snooze_minutes)
        reminder['time'] = snoozed_time.strftime("%Y-%m-%d %H:%M")
        reminder['notified'] = False
        self.logger.info(f"Snoozed reminder: {reminder['text']} to {reminder['time']}")
        print(f"Snoozed reminder: {reminder}")  # Print to verify the snooze action
        self.save_reminders()

    def check_reminders(self) -> None:
        # Check if any reminders are due and snooze them
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        for reminder in self.reminders:
            if reminder['time'] <= now and not reminder['notified']:
                self.logger.info(f"Reminder due: {reminder['text']}")
                print(f"Due reminder: {reminder}")  # Print to verify the due reminder
                self.snooze_reminder(reminder, 10)  # Snooze for 10 minutes

    def save_reminders(self) -> None:
        # Save reminders to a file
        with open('snooze_reminders.json', 'w') as f:
            json.dump(self.reminders, f)
        self.logger.info("Reminders saved to snooze_reminders.json")
        print("Reminders saved to snooze_reminders.json")  # Print for confirmation

    def load_reminders(self) -> None:
        # Load reminders from a file
        try:
            with open('snooze_reminders.json', 'r') as f:
                self.reminders = json.load(f)
            self.logger.info("Reminders loaded from snooze_reminders.json")
        except FileNotFoundError:
            self.reminders = []
            self.logger.info("No previous reminders found. Starting fresh.")
            print("No previous reminders found. Starting fresh.")  # Print for confirmation

if __name__ == "__main__":
    context = None  # Simulated context for testing
    manager = SnoozeReminderManager(context)
    
    # Example actions:
    manager.add_reminder("Morning Meeting", "2023-09-21 10:00")
    manager.check_reminders()

    # Print out reminders to verify snooze functionality
    print(f"Reminders after checking: {manager.reminders}")
