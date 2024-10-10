import speech_recognition as sr
from googletrans import Translator

def recognize_speech_from_mic():
    # Initialize recognizer and translator
    recognizer = sr.Recognizer()
    translator = Translator()

    # Set up microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise to improve recognition
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Shorter adjustment time
        print("Listening for speech...")

        # Capture audio from the microphone
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Set timeouts
            # Convert audio input from speech to text
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"Recognized text: {text}")
            
            # Translate the recognized text to English (if needed)
            translated_text = translator.translate(text, dest='en').text
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
    while True:
        recognized_text = recognize_speech_from_mic()
        if recognized_text:
            # Exit loop if user says "exit" or "stop"
            if recognized_text.lower() in ["exit", "stop"]:
                print("Exiting the speech recognition loop.")
                break
            else:
                print(f"Processing recognized text: {recognized_text}")
