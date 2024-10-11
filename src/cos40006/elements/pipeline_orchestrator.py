import aiko_services as aiko
from typing import Tuple, Any, Dict
import json

class PipelineOrchestrator(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("orchestrator:0")
        context.get_implementation("PipelineElement").__init__(self, context)
        self.llm_response = None

    def process_frame(self, stream: Any, frame: Dict[str, Any] = None, **kwargs) -> Tuple[aiko.StreamEvent, Dict[str, Any]]:
        self.logger.info(f"Orchestrator received input: {frame}")
        
        if self.llm_response is None:
            # Initial processing
            text = frame.get('text') if frame else kwargs.get('text')
            if not text:
                return aiko.StreamEvent.ERROR, {"error": "No input text provided"}

            self.logger.info(f"Orchestrator passing text to LLMElement: {text}")
            return aiko.StreamEvent.OKAY, {"text": text}
        else:
            # Final processing
            try:
                parsed_response = json.loads(self.llm_response)
            except json.JSONDecodeError:
                return aiko.StreamEvent.ERROR, {"error": "Invalid JSON in LLM response"}

            # Here you can add logic to handle reminder_details and emotion_details if needed

            self.logger.info(f"Orchestrator output: {parsed_response}")
            self.llm_response = None  # Reset for the next request
            return aiko.StreamEvent.OKAY, {"orchestrated_response": json.dumps(parsed_response)}

    def set_llm_response(self, response):
        self.llm_response = response

    def start(self):
        self.logger.info("PipelineOrchestrator started")

    def stop(self):
        self.logger.info("PipelineOrchestrator stopped")
