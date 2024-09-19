import aiko_services as aiko
from typing import List, Dict
from datetime import datetime, timedelta
import logging
import json

class RecurringReminderManager(aiko.PipelineElement):
    def __init__(self, context):
        # Only set protocol and initialize with context if context is provided
        if context:
            context.set_protocol("recurring_reminder:0")
            context.get_implementation("PipelineElement").__init__(self, context)

        # Initialize the reminder manager without context dependency
        self.reminders: List[Dict[str, str]] = []
        self.logger = logging.getLogger("RecurringReminderManager")
        self.load_reminders()

    def add_recurring_reminder(self, text: str, start_time: str, interval: str) -> None:
        reminder = {'text': text, 'time': start_time, 'interval': interval, 'notified': False}
        self.reminders.append(reminder)
        self.logger.info(f"Added reminder: {text} at {start_time} every {interval}")
        print(f"Reminder added: {reminder}")  # Debug print
        self.save_reminders()

    def check_reminders(self) -> List[Dict[str, str]]:
        now = datetime.now()
        due_reminders = [r for r in self.reminders if datetime.strptime(r['time'], "%Y-%m-%d %H:%M") <= now and not r['notified']]
        for reminder in due_reminders:
            self.logger.info(f"Reminder due: {reminder['text']}")
            print(f"Due reminder: {reminder}")  # Debug print
            self.notify_user(reminder['text'])
            self.reschedule_reminder(reminder)
        return due_reminders

    def reschedule_reminder(self, reminder: Dict[str, str]) -> None:
        reminder_time = datetime.strptime(reminder['time'], "%Y-%m-%d %H:%M")
        if reminder['interval'] == "daily":
            new_time = reminder_time + timedelta(days=1)
        elif reminder['interval'] == "weekly":
            new_time = reminder_time + timedelta(weeks=1)
        else:
            return
        reminder['time'] = new_time.strftime("%Y-%m-%d %H:%M")
        reminder['notified'] = False
        self.logger.info(f"Rescheduled reminder: {reminder['text']} to {reminder['time']}")
        print(f"Rescheduled reminder: {reminder}")  # Debug print
        self.save_reminders()

    def notify_user(self, message: str) -> None:
        self.logger.info(f"Notifying user: {message}")

    def save_reminders(self) -> None:
        with open('recurring_reminders.json', 'w') as f:
            json.dump(self.reminders, f)

    def load_reminders(self) -> None:
        try:
            with open('recurring_reminders.json', 'r') as f:
                self.reminders = json.load(f)
        except FileNotFoundError:
            self.reminders = []

if __name__ == "__main__":
    context = None  # Simulated context for now
    manager = RecurringReminderManager(context)
    
    # Example actions:
    manager.add_recurring_reminder("Daily Meeting", "2023-09-21 10:00", "daily")
    manager.check_reminders()
