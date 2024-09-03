import speech_recognition as sr
from googletrans import Translator

def recognize_speech_from_mic(language="en-US"):
    # Initialize recognizer and translator
    recognizer = sr.Recognizer()
    translator = Translator()

    # Set up microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise to improve recognition
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Shorter adjustment time
        print("Listening for speech...")

        # Capture audio from the microphone with a timeout and phrase time limit
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Set timeouts
            # Convert audio input from speech to text with specified language
            text = recognizer.recognize_google(audio, language=language)
            print(f"Recognized text in {language}: {text}")
            
            # Translate the recognized text to English
            translated_text = translator.translate(text, src=language, dest='en').text
            print(f"Translated text: {translated_text}")
            return translated_text
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

if __name__ == "__main__":
    print("Enter the language code (e.g., 'en-US' for English, 'es-ES' for Spanish, 'bn-BD' for Bangla (Bengali)): ")
    language_code = input("Language code: ")

    while True:
        recognized_text = recognize_speech_from_mic(language=language_code)
        if recognized_text:
            # Send text to other modules, notifications, emotion detection, etc.
            # Exit loop if user says "exit" or "stop" in the selected language
            if recognized_text.lower() in ["exit", "stop"]:
                print("Exiting the speech recognition loop.")
                break
            else:
                print(f"Processing recognized text: {recognized_text}")
