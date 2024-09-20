import unittest
from .text_to_speech_element import TextToSpeechElement
from .context import ContextManager
import aiko_services as aiko

class TestTextToSpeechElement(unittest.TestCase):

    def setUp(self):
        context = ContextManager()  # Initialize the context
        self.text_to_speech = TextToSpeechElement(context)

    def test_process_frame_with_text(self):
        frame = {"text": "Hello World"}
        event, output = self.text_to_speech.process_frame(None, frame)
        
        # Check if the event is OKAY
        self.assertEqual(event, aiko.StreamEvent.OKAY)
        
        # Check if the speech is correctly simulated
        self.assertIn("speech_output", output)
        self.assertEqual(output["speech_output"], "Simulated speech: Hello World")
    
    def test_process_frame_without_text(self):
        frame = {}
        event, output = self.text_to_speech.process_frame(None, frame)
        
        # Check if the event is OKAY despite no text
        self.assertEqual(event, aiko.StreamEvent.OKAY)
        
        # Check if the frame is passed through unchanged
        self.assertEqual(output, frame)

if __name__ == '__main__':
    unittest.main()
