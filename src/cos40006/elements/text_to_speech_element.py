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
        
        
        

        
        
        
        
        

