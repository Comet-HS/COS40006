import pyttsx3  # Importing the text-to-speech library
import logging
import threading
from queue import Queue

class TextToSpeechElement:
    def __init__(self, context=None):
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        self.logger = logging.getLogger(__name__)
        self.speech_queue = Queue()
        self.is_speaking = threading.Event()  # Event to track if TTS is speaking

        # Start a thread to handle the speech queue
        self.speech_thread = threading.Thread(target=self.process_speech_queue, daemon=True)
        self.speech_thread.start()

        # Bind the "finished-utterance" event to callback function
        self.engine.connect('finished-utterance', self.on_speech_finished)

    def add_to_queue(self, text):
        """Add the text to the speech queue."""
        self.logger.info(f"Queueing text for speech: {text}")
        self.speech_queue.put(text)

    def process_speech_queue(self):
        """Process the speech queue by converting text to speech sequentially."""
        while True:
            text = self.speech_queue.get()  # Wait for the next text in the queue
            if text:
                try:
                    self.logger.info(f"Speaking text: {text}")
                    self.is_speaking.set()  # Mark as speaking
                    self.engine.say(text)
                    self.engine.runAndWait()  # Block until speech is finished
                except Exception as e:
                    self.logger.error(f"Error during speech synthesis: {e}")
                finally:
                    self.speech_queue.task_done()

    def process_frame(self, stream: dict = None, frame: dict = None, **kwargs):
        """Process the frame by converting the text in it to speech."""
        self.logger.debug(f"TextToSpeechElement process_frame called with: stream={stream}, frame={frame}, kwargs={kwargs}")

        if frame is None:
            frame = kwargs

        text = frame.get("text") or frame.get("general_text") or frame.get("processed_reminder") or frame.get("detected_emotion")
        
        if text is None:
            self.logger.warning("No text provided in the frame")
            return {"status": "OK", "frame": frame}
        
        # Log the conversion event
        self.logger.info(f"Converting to speech: {text}")
        
        # Add the text to the queue for speech processing
        self.add_to_queue(text)
        
        return {"speech_output": f"Queued speech: {text}"}

    def on_speech_finished(self, name, completed):
        """Callback when speech is finished."""
        self.logger.info(f"Speech finished: {name}, completed: {completed}")
        self.is_speaking.clear()  # Mark as not speaking

    def speak_text(self, text: str):
        """Queue text for speech to avoid skipping when engine is busy."""
        self.logger.info(f"Queueing text for speech: {text}")
        self.add_to_queue(text)  # Add text to the queue
    

# Optional test block if run standalone
if __name__ == "__main__":
    # Standalone test for the TextToSpeechElement
    logging.basicConfig(level=logging.DEBUG)
    tts = TextToSpeechElement()
    tts.speak_text("This is a test of the text-to-speech engine.")
    tts.speak_text("This is the second test.")
    tts.speak_text("This is the third test.")
