import aiko_services as aiko
import speech_recognition as sr
from googletrans import Translator
import logging
from typing import Tuple

# Initialize logging for this script
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElementDefinition:
    """ Mimic the structure expected for element definitions. """
    def __init__(self, input, output):
        self.input = input
        self.output = output

class SpeechToTextElement(aiko.PipelineElement):
    def __init__(self, context):
        super().__init__()  # Correct parent class initialization
        
        # Define the input/output structure expected by Aiko
        self.definition = ElementDefinition(
            input=[{'name': 'audio_input', 'type': 'audio'}],
            output=[{'name': 'recognized_text', 'type': 'str'}]
        )
        
        # Set up the recognizer and translator
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        logger.info("SpeechToTextElement has been initialized.")

    def process_frame(self, stream, frame=None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        logger.info("process_frame() called")
        try:
            with sr.Microphone() as source:
                logger.info("Microphone initialized. Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                logger.info("Listening for speech...")

                # Capture audio with a timeout and phrase time limit
                audio_data = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                logger.info("Audio has been captured.")

                # Recognize speech
                recognized_text = self.recognizer.recognize_google(audio_data)
                logger.info(f"Recognized text: {recognized_text}")

                # Translate the recognized text
                translated_text = self.translator.translate(recognized_text, dest='en').text
                logger.info(f"Translated text: {translated_text}")

                # Return the recognized text and translated text
                return aiko.StreamEvent.OKAY, {"recognized_text": recognized_text, "translated_text": translated_text}

        except sr.WaitTimeoutError:
            logger.error("Listening timed out while waiting for phrase to start.")
            return aiko.StreamEvent.ERROR, {"recognized_text": "Error: Timeout"}
        except sr.UnknownValueError:
            logger.error("Could not understand the audio.")
            return aiko.StreamEvent.ERROR, {"recognized_text": "Error: Unknown Value"}
        except sr.RequestError as e:
            logger.error(f"Error with Google Web API: {e}")
            return aiko.StreamEvent.ERROR, {"recognized_text": f"Error: {e}"}

# Required method for Aiko framework
def get_implementations():
    return {"SpeechToTextElement": SpeechToTextElement}
