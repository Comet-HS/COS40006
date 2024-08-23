import schedule
import time
from datetime import datetime

class ReminderSystem:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, time_str, message):
        # Add a new reminder
        reminder_time = datetime.strptime(time_str, "%H:%M")
        self.reminders.append((reminder_time, message))
        schedule.every().day.at(time_str).do(self.trigger_reminder, message)
        print(f"Reminder set for {time_str}: {message}")

    def trigger_reminder(self, message):
        # Trigger the reminder
        print(f"Reminder: {message}")
        self.send_reminder_to_robot(message)

    def send_reminder_to_robot(self, message):
        # Send the reminder to the robot dog (Placeholder function)
        print(f"Sending reminder to robot: {message}")

    def run(self):
        # Run the scheduler to process reminders
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    reminder_system = ReminderSystem()
    
    # Sample reminders
    reminder_system.add_reminder("11:00", "Take your medication.")
    reminder_system.add_reminder("14:00", "Time for a short walk!")
    reminder_system.add_reminder("20:30", "Prepare for bed.")
    
    # Start the reminder system
    reminder_system.run()
