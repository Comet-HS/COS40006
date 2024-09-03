import aiko_services as aiko
from typing import Tuple, Any

class EmotionDetectionElement(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("emotion:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.debug(f"EmotionDetectionElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")
        
        if frame is None:
            frame = kwargs

        emotion_text = frame.get("emotion_text")
        if emotion_text is None:
            self.logger.debug("No emotion_text provided in the frame")
            return aiko.StreamEvent.OKAY, frame  # Pass through the frame

        self.logger.info(f"Detecting emotion in: {emotion_text}")
        # Simple emotion detection
        return aiko.StreamEvent.OKAY, {"detected_emotion": "neutral"}
