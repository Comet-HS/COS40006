import aiko_services as aiko
from typing import Tuple, Any, Dict
import json

class PipelineOrchestrator(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("orchestrator:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream: Any, frame: Dict[str, Any] = None, **kwargs) -> Tuple[aiko.StreamEvent, Dict[str, Any]]:
        self.logger.info(f"Orchestrator received input: {frame}")
        
        # Extract text from frame or kwargs
        text = frame.get('text') if frame else kwargs.get('text')
        if not text:
            return aiko.StreamEvent.ERROR, {"error": "No input text provided"}

        # For now, we'll just pass the input directly to the LLM
        # In the future, we can add logic here to route to different elements
        return aiko.StreamEvent.OKAY, {"text": text}

    def start(self):
        self.logger.info("PipelineOrchestrator started")

    def stop(self):
        self.logger.info("PipelineOrchestrator stopped")
