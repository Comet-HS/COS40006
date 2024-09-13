import aiko_services as aiko
from typing import Tuple
import speech_recognition as sr

recognizer = sr.Recognizer()

class AudioInput(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("audio:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream, data) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.info(f"Received data: {data}")
        with sr.Microphone() as source:
            self.logger.info("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            self.logger.info("Listening for speech...")
            audio_input = recognizer.listen(source)
        return aiko.StreamEvent.OKAY, {"audio_data": audio_input}
    
class SpeechToText(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("speechtotext:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream, audio_data) -> Tuple[aiko.StreamEvent, dict]:
        
        
        text = recognizer.recognize_google(audio_data)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text}")
            return aiko.StreamEvent.OKAY, {"converted_text": text}
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None
       

