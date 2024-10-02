import google.generativeai as genai
import os
import json
import datetime
import re

genai.configure(api_key=os.environ["API_KEY"])

class VoiceAssistant:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.chat = self.model.start_chat(history=[])
        self.initialize_assistant()

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
        Do not set reminders without having the full details about the reminder. Do not set reminders for the dates that
        have already passed.

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

    def process_input(self, user_input):
        current_time = datetime.datetime.now()
        time_info = f"Current date and time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        full_input = f"{time_info}\nUser input: {user_input}"
        
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
        
        return parsed_response

def test_llm():
    assistant = VoiceAssistant()
    print("Voice Assistant: Hello! How can I help you today?")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Voice Assistant: Goodbye! Have a great day!")
                break

            result = assistant.process_input(user_input)
            
            if result.get("reminder_details"):
                print(f"Voice Assistant: I've set a reminder: {result['reminder_details']['details']} on {result['reminder_details']['date']} at {result['reminder_details']['time']}")
            if result.get("emotion_details"):
                print(f"Voice Assistant: I sense {result['emotion_details']['emotion']} in your message.")
            
            response = result.get('response', "I'm not sure how to respond to that.")
            print(f"Voice Assistant: {response}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_llm()