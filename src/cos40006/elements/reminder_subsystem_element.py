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

        self.logger.info(f"Processing reminder: {reminder_text}")
        # Simple reminder processing
        return aiko.StreamEvent.OKAY, {"processed_reminder": f"Reminder set: {reminder_text}"}
