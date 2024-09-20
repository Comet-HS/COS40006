import aiko_services as aiko
from typing import Tuple

class UpperText(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("upper:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream, text) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.info(f"received text: {text}")
        upper_case = text.upper()
        self.logger.info(f"processed text: {upper_case}")
        return aiko.StreamEvent.OKAY, {"upper_case_text": upper_case}
        # return super().process_frame(stream, **kwargs)


class ReverseText(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("reverse:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream, upper_case_text) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.info(f"received text: {upper_case_text}")
        reverse_text = upper_case_text[::-1]
        self.logger.info(f"processed text: {reverse_text}")
        return aiko.StreamEvent.OKAY, {"reversed_text": reverse_text} 
        # return super().process_frame(stream, **kwargs)
    