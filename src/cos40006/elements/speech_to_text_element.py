import aiko_services as aiko
import speech_recognition as sr
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("speech_to_text_element.py has been loaded successfully.")

class SpeechToTextElement(aiko.PipelineElement):
    def __init__(self, context):
        if context:
            context.set_protocol("speech_to_text:0")
            context.get_implementation("PipelineElement").__init__(self, context)
        self.recognizer = sr.Recognizer()

    def process_frame(self, stream, frame=None, **kwargs):
        logger.debug("Processing frame in SpeechToTextElement.")
        try:
            # Listen to microphone input
            with sr.Microphone() as source:
                logger.debug("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source)
                logger.debug("Listening for speech...")
                audio_data = self.recognizer.listen(source)

                # Convert speech to text using Google Web API
                recognized_text = self.recognizer.recognize_google(audio_data, language="en-US")
                logger.debug(f"Recognized text: {recognized_text}")

                # Return the recognized text
                return aiko.StreamEvent.OKAY, {"text_output": recognized_text}

        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return aiko.StreamEvent.ERROR, frame

# Required method for Aiko framework
def get_implementations():
    return {"SpeechToTextElement": SpeechToTextElement}
