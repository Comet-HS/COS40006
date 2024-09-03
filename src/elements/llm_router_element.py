import aiko_services as aiko
from typing import Tuple, Any

class LLMRouterElement(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("llm_router:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.debug(f"LLMRouterElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")
        
        if frame is None:
            frame = kwargs

        text = frame.get("text", "")
        self.logger.info(f"Routing text: {text}")
        
        # Return all possible outputs, with None for unused routes
        return aiko.StreamEvent.OKAY, {
            "reminder_text": text if "reminder" in text.lower() else None,
            "emotion_text": text if "emotion" in text.lower() else None,
            "general_text": text
        }
