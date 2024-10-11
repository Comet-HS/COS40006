import aiko_services as aiko
import speech_recognition as sr
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
        super().__init__()
        
        # Define the input/output structure expected by Aiko
        self.definition = ElementDefinition(
            input=[{'name': 'audio_input', 'type': 'audio'}],
            output=[{'name': 'recognized_text', 'type': 'str'}]
        )
        
        # Set up the recognizer
        self.recognizer = sr.Recognizer()
        logger.info("speech_to_text has been initialized")

    def process_frame(self, stream, frame=None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        logger.info("Listening for speech")
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise and listen for speech
                self.recognizer.adjust_for_ambient_noise(source, duration= 2)
                logger.info("Microphone adjusted for ambient noise.")
                
                # Capture audio with a timeout and phrase time limit
                audio_data = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                logger.info("Captured Speech")

                # Recognize speech using Google's speech recognition service
                recognized_text = self.recognizer.recognize_google(audio_data)
                logger.info(f"Recognized Speech: {recognized_text}")

                # Check for stop conditions
                if recognized_text.lower() in ["stop", "quit"]:
                    logger.info("Stop command received. Exiting...")
                    return aiko.StreamEvent.OKAY, {"recognized_text": "Exiting loop"}

                # Return the recognized text as part of the stream event
                return aiko.StreamEvent.OKAY, {"recognized_text": recognized_text}

        except sr.WaitTimeoutError:
            logger.info("User inactive for too long. Exiting...")
            return aiko.StreamEvent.ERROR, {"recognized_text": "Timeout - User Inactive"}
        except sr.UnknownValueError:
            logger.info("Could not understand the audio")
            return aiko.StreamEvent.ERROR, {"recognized_text": "Unknown Value"}
        except sr.RequestError as e:
            logger.error(f"Error with Google Web API: {e}")
            return aiko.StreamEvent.ERROR, {"recognized_text": f"Error: {e}"}

    # Implement abstract methods with placeholders
    def add_message_handler(self, *args, **kwargs):
        pass

    def add_tags(self, *args, **kwargs):
        pass

    def add_tags_string(self, *args, **kwargs):
        pass

    def create_frame(self, *args, **kwargs):
        pass

    def create_frames(self, *args, **kwargs):
        pass

    def get_parameter(self, *args, **kwargs):
        pass

    def get_stream(self, *args, **kwargs):
        pass

    def get_stream_parameters(self, *args, **kwargs):
        pass

    def get_tags_string(self, *args, **kwargs):
        pass

    def my_id(self, *args, **kwargs):
        pass

    def registrar_handler_call(self, *args, **kwargs):
        pass

    def remove_message_handler(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

    def set_registrar_handler(self, *args, **kwargs):
        pass

    def start_stream(self, *args, **kwargs):
        pass

    def stop(self, *args, **kwargs):
        pass

    def stop_stream(self, *args, **kwargs):
        pass

# Required method for Aiko framework
def get_implementations():
    return {"SpeechToTextElement": SpeechToTextElement}

# Add a main function to allow standalone execution
if __name__ == '__main__':
    logger.info("Starting SpeechToTextElement as a standalone application...")
    element = SpeechToTextElement(context={})
    
    # Simulate a stream for testing purposes
    stream = {"stream_id": "*"}
    while True:
        result_event, result_data = element.process_frame(stream)
        
        # Break the loop if the user says "stop" or "quit" or there's a timeout
        if result_event == aiko.StreamEvent.ERROR or result_data.get("recognized_text", "").lower() in ["exiting loop", "timeout - user inactive"]:
            break

    logger.info("Speech recognition process has ended.")
