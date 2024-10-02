import aiko_services as aiko
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("console_output_element.py has been loaded successfully.")

class ConsoleOutputElement(aiko.PipelineElement):
    def __init__(self, context):
        if context:
            context.set_protocol("console_output:0")
            context.get_implementation("PipelineElement").__init__(self, context)
        logger.debug("ConsoleOutputElement initialized.")

    def process_frame(self, stream, frame=None, **kwargs):
        logger.debug("Processing frame in ConsoleOutputElement.")
        text_output = frame.get("text_output", "")
        emotion_output = frame.get("emotion_output", "")
        reminder_output = frame.get("reminder_output", "")
        
        # Print the outputs to the console
        print(f"Recognized Text: {text_output}")
        print(f"Detected Emotion: {emotion_output}")
        print(f"Reminder Output: {reminder_output}")
        return aiko.StreamEvent.OKAY, frame

# Required method for Aiko framework
def get_implementations():
    return {"ConsoleOutputElement": ConsoleOutputElement}
