import speech_recognition as sr

def recognize_speech_from_mic():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Set up microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise to improve recognition
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for speech...")

        # Capture audio from the microphone
        audio = recognizer.listen(source)

        # Convert audio input from speech to text)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

if __name__ == "__main__":
    while True:
        recognized_text = recognize_speech_from_mic()
        if recognized_text:
            # send text to other modules, notification, emotion detection, etc.
            pass
