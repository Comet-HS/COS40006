import aiko_services as aiko
from typing import Tuple

class PE_SpeechtoText(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("speech:0")
        context.get_implementation("PipelineElement").__init__(self, context)


    def process_frame(self, stream, speech) -> Tuple[aiko.StreamEvent, dict]:
        #logs into aiko dashboard/terminal
        self.logger.info(f"received speech: {speech}") 
        
        #convert speech to text. For demonstration purposes, we are dealing with text to begin with
        text = speech + " is now text"
        self.logger.info(f"processed speech: {text}") 

        #sends message over to the next element
        return aiko.StreamEvent.OKAY, {"text": text}
    



class PE_LLM(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("llm:0")
        context.get_implementation("PipelineElement").__init__(self, context)


    def process_frame(self, stream, text) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.info(f"received text: {text}")

        #LLM Logic placeholder
        if "remind" in text:
            #todo: need to process the actual reminder.
            reminder = "send_reminder"
            self.logger.info("reminder detected")
            return aiko.StreamEvent.OKAY, {"reminder": reminder}
        else:
            #todo: need to be able to actually detect emotion
            emotion = "send_emotion"
            self.logger.info("emotion detected")
            return aiko.StreamEvent.OKAY, {"emotion": emotion}
        



        

