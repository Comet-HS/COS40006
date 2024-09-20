import aiko_services as aiko
from typing import Tuple

 # Run test with frame data
 # aiko_pipeline create emotion_pipeline.json --frame_data "(emotion_text: 'I am very happy today!')"

 # Can't load module?
 # 

 # To Do
 # once working, correct file paths to appropriate directory.


class EmotionDetectionElement(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("emotion:0")
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream, emotion_text) -> Tuple[aiko.StreamEvent, dict]:

        self.logger.debug(f"received text: {emotion_text}")

        # Detect the emotion
        detected_emotion = self.detect_emotion(emotion_text)
        self.logger.info(f"Detected emotion: {detected_emotion}")

        # Return the detected emotion
        return aiko.StreamEvent.OKAY, {"detected_emotion": detected_emotion}

    def detect_emotion(self, text: str) -> str:
        # Simple keyword-based detection
        emotion_map = {
            "happy": "happy",
            "joy": "happy",
            "excited": "happy",
            "sad": "sad",
            "angry": "angry",
            "frustrated": "angry",
            "scared": "fear",
            "afraid": "fear"
        }

        for keyword, emotion in emotion_map.items():
            if keyword in text.lower():
                return emotion
        return "neutral"