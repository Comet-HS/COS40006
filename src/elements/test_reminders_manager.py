import unittest
from reminders_manager import ReminderManager

class TestReminderManager(unittest.TestCase):
    def setUp(self):
        """
        This method runs before each test, initializing the ReminderManager.
        """
        self.reminder_manager = ReminderManager()

    def test_add_reminder(self):
        """
        Test if a reminder can be added to the ReminderManager.
        """
        self.reminder_manager.add_reminder("Test reminder", "2024-09-11 12:00")
        reminders = self.reminder_manager.get_reminders()
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0]['text'], "Test reminder")
        self.assertEqual(reminders[0]['time'], "2024-09-11 12:00")

    def test_check_due_reminders(self):
        """
        Test if the check_reminders method correctly identifies due reminders.
        """
        # Add a reminder that is already due
        self.reminder_manager.add_reminder("Due reminder", "2024-09-10 12:00")
        due_reminders = self.reminder_manager.check_reminders()
        self.assertTrue(len(due_reminders) > 0)
        self.assertEqual(due_reminders[0]['text'], "Due reminder")

    def test_save_and_load_reminders(self):
        """
        Test if reminders can be saved and loaded from a file.
        """
        # Add a reminder and save it
        self.reminder_manager.add_reminder("Saved reminder", "2024-09-12 10:00")
        self.reminder_manager.save_reminders()

        # Create a new ReminderManager instance to simulate a fresh start
        new_manager = ReminderManager()
        reminders = new_manager.get_reminders()
        
        # Check if the loaded reminder matches the one saved
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0]['text'], "Saved reminder")
        self.assertEqual(reminders[0]['time'], "2024-09-12 10:00")

if __name__ == "__main__":
    unittest.main()
