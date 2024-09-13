#PipelineElement creation template

import aiko_services as aiko
from typing import Tuple

class ElementName(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("protocol_name:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    #do your normal logic/methods here


    #This method captures and sends over data to & from elements
    def process_frame(self, stream, data) -> Tuple[aiko.StreamEvent, dict]:
        
        #logs into aiko dashboard/terminal
        self.logger.info(f"received data: {data}") 
        
        #do something with the data here. This is just an example
        processed_data = data
        self.logger.info(f"processed data: {processed_data}") 

        #sends message over to the next element
        return aiko.StreamEvent.OKAY, {"processed_data": processed_data}
