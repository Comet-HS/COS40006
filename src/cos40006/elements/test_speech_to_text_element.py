import unittest
from speech_to_text_element import SpeechToTextElement

from .context import ContextManager
import aiko_services as aiko

class TestSpeechToTextElement(unittest.TestCase):

    def setUp(self):
        context = ContextManager()  # Initialize the context
        self.speech_to_text = SpeechToTextElement(context)

    def test_process_frame_with_audio(self):
        frame = {"audio": "Hello World"}
        event, output = self.speech_to_text.process_frame(None, frame)
        
        # Check if the event is OKAY
        self.assertEqual(event, aiko.StreamEvent.OKAY)
        
        # Check if the text is correctly converted
        self.assertIn("text", output)
        self.assertEqual(output["text"], "Simulated speech-to-text: Hello World")

if __name__ == '__main__':
    unittest.main()
