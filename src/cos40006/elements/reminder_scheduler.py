# reminder_scheduler.py
import time
from reminder_manager import ReminderManager

def run_scheduler():
    reminder_manager = ReminderManager()
    reminder_manager.load_reminders()

    while True:
        reminder_manager.check_reminders()
        time.sleep(60)  # Check reminders every minute

if __name__ == '__main__':
    run_scheduler()
