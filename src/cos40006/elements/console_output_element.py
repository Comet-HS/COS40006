import aiko_services as aiko
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsoleOutputElement(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("console_output:0")
        super().__init__(context)
        logger.info("ConsoleOutputElement initialized.")

    def process_frame(self, stream, frame=None, **kwargs):
        logger.info(f"Received frame: {frame}")
        print(f"Console Output - Recognized: {frame.get('recognized_text')}, Translated: {frame.get('translated_text')}")
        return aiko.StreamEvent.OKAY, frame

# Required method for Aiko framework
def get_implementations():
    return {"ConsoleOutputElement": ConsoleOutputElement}
