import aiko_services as aiko
from typing import Tuple, Any
import pyttsx3  # Importing the text-to-speech library
import logging

class TextToSpeechElement(aiko.PipelineElement):
    import logging

class TextToSpeechElement(aiko.PipelineElement):
    def __init__(self, context):
        # Initialize the TTS engine and set protocol
        self.engine = pyttsx3.init()  # Initialize the TTS engine
        context.set_protocol("text_to_speech:0")
        context.get_implementation("PipelineElement").__init__(self, context)
        
        # Initialize logger with a fallback to a basic logger
        self.logger = getattr(context, 'logger', logging.getLogger(__name__))

        try:
            self.logger.info("Initializing pyttsx3.")
            self.speak_text("Hello, this is a text-to-speech test.")
        except Exception as e:
            self.logger.error(f"Error initializing pyttsx3: {e}")

        


    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.debug(f"TextToSpeechElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")

        if frame is None:
            frame = kwargs

        text = frame.get("text") or frame.get("general_text") or frame.get("processed_reminder") or frame.get("detected_emotion")
        
        if text is None:
            self.logger.warning("No text provided in the frame")
            return aiko.StreamEvent.OKAY, frame
        
        # Log the conversion event
        self.logger.info(f"Converting to speech: {text}")
        
        # Simulate text-to-speech conversion
        self.speak_text(text)  # Call the speak_text method to convert text to speech
        
        return aiko.StreamEvent.OKAY, {"speech_output": f"Simulated speech: {text}"}

    def speak_text(self, text: str):
        """This method uses pyttsx3 to convert text to audible speech."""
        try:
            self.logger.info(f"Speaking text: {text}")  # Log the text being spoken
            self.engine.say(text)  # Queue the speech
            self.engine.runAndWait()  # Play the speech
        except Exception as e:
            self.logger.error(f"Error during speech synthesis: {e}")
      
        
    # Empty implementations for abstract methods
    def add_message_handler(self, *args, **kwargs): pass
    def add_tags(self, *args, **kwargs): pass
    def add_tags_string(self, *args, **kwargs): pass
    def create_frame(self, *args, **kwargs): pass
    def create_frames(self, *args, **kwargs): pass
    def get_parameter(self, *args, **kwargs): pass
    def get_stream(self, *args, **kwargs): pass
    def get_stream_parameters(self, *args, **kwargs): pass
    def get_tags_string(self, *args, **kwargs): pass
    def my_id(self, *args, **kwargs): pass
    def registrar_handler_call(self, *args, **kwargs): pass
    def remove_message_handler(self, *args, **kwargs): pass
    def run(self, *args, **kwargs): pass
    def set_registrar_handler(self, *args, **kwargs): pass
    def start_stream(self, *args, **kwargs): pass
    def stop(self, *args, **kwargs): pass
    def stop_stream(self, *args, **kwargs): pass 
    
    
    
if __name__ == "__main__":
    # Standalone test for the TextToSpeechElement
    engine = pyttsx3.init()
    
    def speak_text(text):
        engine.say(text)
        engine.runAndWait()
    
    # Test the method
    speak_text("This is a test of the text-to-speech engine.")    
     

        

        
        
        

