import aiko_services as aiko
from typing import Tuple, Any

class SpeechToTextElement(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("speech_to_text:0")
        context.get_implementation("PipelineElement").__init__(self, context)
        self.logger.debug("SpeechToTextElement initialized")

    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.debug(f"SpeechToTextElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")
        
        if frame is None:
            frame = kwargs

        audio = frame.get('audio', '')
        self.logger.debug(f"Processing audio: {audio}")
        
        # Simulate speech-to-text conversion
        text = f"Simulated speech-to-text: {audio}"
        self.logger.info(f"Converted speech to text: {text}")
        
        return aiko.StreamEvent.OKAY, {"text": text}
