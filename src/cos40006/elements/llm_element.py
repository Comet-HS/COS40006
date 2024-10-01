import aiko_services as aiko
from typing import Tuple, Any
import google.generativeai as genai
import os
import json
import datetime

genai.configure(api_key=os.environ["API_KEY"])

class LLMElement(aiko.PipelineElement):
    def __init__(self, context):
        context.set_protocol("llm:0")
        context.get_implementation("PipelineElement").__init__(self, context)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[])
        self.initialize_assistant()
        self.logger.debug("LLMElement initialized")

    def initialize_assistant(self):
        system_prompt = """
        You are a helpful voice assistant in the form of a robot dog. Your capabilities include:
        1. Setting reminders
        2. Detecting emotions in text
        3. Answering general questions
        4. Engaging in friendly conversation

        For each user input, you should:
        1. Determine the intent of the user's request (reminder, emotion, or general)
        2. Provide an appropriate response

        If the user wants to set a reminder, you should:
        1. Ask for the reminder details (e.g. date, time, and what to remind them of) if not already provided
        2. Store the reminder details
        3. Provide a confirmation to the user

        The reminder details should be stored in a structured format, such as a dictionary with keys for the date,
        time, if it should be repeated, and the reminder details.
        Do not set reminders without having the full details about the reminder.

        You should also be able to detect emotions in text when relevant.

        Always be polite, concise, and helpful. If you're asked to do something 
        outside your capabilities, kindly explain what you can do instead.

        Do not use emojis in your responses.

        Respond ONLY in the following JSON format, with no additional text before or after:
        {
            "reminder_details": {"date": "YYYY-MM-DD", "time": "HH:MM", "repeat": boolean, "details": "string"} or null if not applicable,
            "emotion_details": {"emotion": "string", "confidence": "string"} or null if not applicable,
            "response": "Your response to the user"
        }
        """
        self.chat.send_message(system_prompt)

    def process_frame(self, stream: Any, text: str) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.info(f"Processing user input: {text}")

        current_time = datetime.datetime.now()
        time_info = f"Current date and time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        full_input = f"{time_info}\nUser input: {text}"
        
        response = self.chat.send_message(full_input)
        try:
            parsed_response = json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback in case the LLM doesn't produce valid JSON
            parsed_response = {
                "reminder_details": None,
                "emotion_details": None,
                "response": response.text
            }
        
        self.logger.info(f"LLM response: {parsed_response}")
        
        return aiko.StreamEvent.OKAY, parsed_response

    def start(self):
        self.logger.info("LLMElement started")

    def stop(self):
        self.logger.info("LLMElement stopped")
