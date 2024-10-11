import aiko_services as aiko
from typing import Tuple, Any
import google.generativeai as genai
import os
import json
import datetime

genai.configure(api_key="AIzaSyB4eCh_dTUMyASbCmMMgDotVN-MLMSyML4")

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

        For each user input, you MUST:
        1. Determine the intent of the user's request
        2. Provide an appropriate response
        3. Detect emotions in the user's input when you deem it relevant
        4. ALWAYS respond in the exact JSON format specified below, with no additional text before or after

        If the user wants to set a reminder:
        1. Ask for any missing reminder details (date, time, and what to remind them of)
        2. Only set the reminder when all details are provided. DO NOT make up details.
        3. Do not set reminders without having the full details about the reminder.
        4. Do not set reminders for the dates that have already passed.
        5. Provide a confirmation to the user

        For emotion detection:
        1. Include emotion details when you believe it's relevant
        2. Use a confidence scale of 0-100

        ALWAYS respond ONLY in this exact JSON format, with no text before or after:
        {
            "reminder_details": {"date": "YYYY-MM-DD", "time": "HH:MM", "repeat": false, "details": "string"} or null if not applicable,
            "emotion_details": {"emotion": "string", "confidence": number} or null if not applicable,
            "response": "Your response to the user"
        }

        Examples:
        User: "Hello"
        Response:
        {
            "reminder_details": null,
            "emotion_details": null,
            "response": "Hello! I'm your friendly AI assistant. How can I help you today?"
        }

        User: "Set a reminder for tomorrow at 3pm to call mom"
        Response:
        {
            "reminder_details": {"date": "2024-10-03", "time": "15:00", "repeat": false, "details": "call mom"},
            "emotion_details": null,
            "response": "Certainly! I've set a reminder for you to call mom tomorrow at 3:00 PM. Is there anything else you need?"
        }

        User: "I'm feeling really stressed about my upcoming exam"
        Response:
        {
            "reminder_details": null,
            "emotion_details": {"emotion": "stressed", "confidence": 90},
            "response": "I'm sorry to hear that you're feeling stressed about your upcoming exam. It's normal to feel this way. Have you considered some relaxation techniques or creating a study schedule to help manage your stress? Remember, you've prepared for this, and I believe in you!"
        }

        Always maintain this exact JSON structure in your responses, including emotion detection when you deem it relevant.
        """
        self.chat.send_message(system_prompt)

    def process_frame(self, stream: Any, text: str) -> Tuple[aiko.StreamEvent, dict]:
        self.logger.info(f"Processing user input: {text}")

        current_time = datetime.datetime.now()
        time_info = f"Current date and time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        full_input = f"{time_info}\nUser input: {text}"
        
        response = self.chat.send_message(full_input)
        try:
            # Find the first occurrence of '{' and the last occurrence of '}'
            start = response.text.find('{')
            end = response.text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response.text[start:end]
                parsed_response = json.loads(json_str)
            else:
                raise ValueError("No JSON found in the response")

            # Validate the response structure
            assert "reminder_details" in parsed_response
            assert "emotion_details" in parsed_response
            assert "response" in parsed_response
        except Exception as e:
            self.logger.warning(f"Invalid LLM response: {response.text}")
            self.logger.error(f"Error details: {str(e)}")
            parsed_response = {
                "reminder_details": None,
                "emotion_details": None,
                "response": "I apologize, but I encountered an error processing your request. Could you please try again?"
            }
        
        self.logger.info(f"LLM response: {parsed_response}")
        
        return aiko.StreamEvent.OKAY, {"response": json.dumps(parsed_response)}

    def start(self):
        self.logger.info("LLMElement started")

    def stop(self):
        self.logger.info("LLMElement stopped")
