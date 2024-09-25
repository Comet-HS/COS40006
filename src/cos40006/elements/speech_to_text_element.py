import aiko_services as aiko
from typing import Tuple, Any
import speech_recognition as sr  # Using speech_recognition library for speech-to-text

class SpeechToTextElement(aiko.PipelineElement):
    def __init__(self, context):
        # Set protocol and initialize speech recognizer
        context.set_protocol("speech_to_text:0")
        context.get_implementation("PipelineElement").__init__(self, context)
        self.logger.debug("SpeechToTextElement initialized")
        self.recognizer = sr.Recognizer()

    def process_frame(self, stream: Any, frame: dict = None, **kwargs) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.debug(f"SpeechToTextElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")

        if frame is None:
            frame = kwargs

        audio_data = frame.get("audio")

        if audio_data is None:
            self.logger.warning("No audio data provided in the frame")
            return aiko.StreamEvent.OKAY, frame  # Pass through the frame
        
        # Convert audio to text using speech recognition
        try:
            with sr.AudioFile(audio_data) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                self.logger.info(f"Converted audio to text: {text}")
        except Exception as e:
            self.logger.error(f"Failed to convert audio to text: {e}")
            return aiko.StreamEvent.ERROR, frame
        
        return aiko.StreamEvent.OKAY, {"text": text}

if __name__ == "__main__":
    # For testing purposes, mock an audio file input
    context = aiko.ContextManager()
    stt_element = SpeechToTextElement(context)

    # Mock audio data (replace 'path_to_audio.wav' with an actual path)
    mock_frame = {"audio": "path_to_audio.wav"}

    # Call the process_frame method with mock data
    result = stt_element.process_frame(None, mock_frame)
    print(result)
