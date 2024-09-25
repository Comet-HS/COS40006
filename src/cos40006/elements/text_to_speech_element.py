import aiko_services as aiko
from typing import Tuple, Any
import pyttsx3  # Importing the text-to-speech library

class TextToSpeechElement(aiko.PipelineElement):
    def __init__(self, context):
        # Initialize the TTS engine and set protocol
        self.engine = pyttsx3.init()  # Initialize the TTS engine
        context.set_protocol("text_to_speech:0")
        context.get_implementation("PipelineElement").__init__(self, context)
        self.logger.debug("TextToSpeechElement initialized")
        


    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.debug(f"TextToSpeechElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")

        if frame is None:
            frame = kwargs

        text = frame.get("text") or frame.get("general_text") or frame.get("processed_reminder") or frame.get("detected_emotion")
        
        if text is None:
            self.logger.warning("No text provided in the frame")
            return aiko.StreamEvent.OKAY, frame  # Pass through the frame
        
        # Log the conversion event
        self.logger.info(f"Converting to speech: {text}")
        
        # Simulate text-to-speech conversion
        self.speak_text(text)  # Call the speak_text method to convert text to speech
        
        return aiko.StreamEvent.OKAY, {"speech_output": f"Simulated speech: {text}"}

    def speak_text(self, text: str):
        """This method uses pyttsx3 to convert text to audible speech."""
        self.engine.say(text)  # Queue the speech
        self.engine.runAndWait()  # Play the speech
        
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
        

        
        
        
        
        

