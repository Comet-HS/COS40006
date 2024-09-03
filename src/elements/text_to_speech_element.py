import aiko_services as aiko
from typing import Tuple, Any

class TextToSpeechElement(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("text_to_speech:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.debug(f"TextToSpeechElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")
        
        if frame is None:
            frame = kwargs

        text = frame.get("text") or frame.get("general_text") or frame.get("processed_reminder") or frame.get("detected_emotion")
        if text is None:
            self.logger.warning("No text provided in the frame")
            return aiko.StreamEvent.OKAY, frame  # Pass through the frame

        self.logger.info(f"Converting to speech: {text}")
        # Simulate text-to-speech conversion
        return aiko.StreamEvent.OKAY, {"speech_output": f"Simulated speech: {text}"}
