import aiko_services as aiko
from typing import Tuple, Any

class ReminderSubsystemElement(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("reminder:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.debug(f"ReminderSubsystemElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")
        
        if frame is None:
            frame = kwargs

        reminder_text = frame.get("reminder_text")
        if reminder_text is None:
            self.logger.debug("No reminder_text provided in the frame")
            return aiko.StreamEvent.OKAY, frame  # Pass through the frame

        # Process the reminder text to remove the leading phrase like "Set a reminder to"
        stripped_reminder = self.extract_reminder(reminder_text)
        self.logger.info(f"Reminder set: {stripped_reminder}")

        return aiko.StreamEvent.OKAY, {"processed_reminder": stripped_reminder}

    def extract_reminder(self, reminder_text: str) -> str:
        """
        Extract the core reminder from the input text.
        Example:
        Input: "Set a reminder to take medicine at 3 PM"
        Output: "Take medicine at 3 PM"
        """
        if reminder_text.lower().startswith("set a reminder to"):
            return reminder_text[17:].strip().capitalize()
        return reminder_text.capitalize()

if __name__ == "__main__":
    context = None  # Simulated context for testing
    element = ReminderSubsystemElement(context)
    print("ReminderSubsystemElement loaded successfully")
