import speech_recognition as sr

def take_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise before starting to listen
        r.adjust_for_ambient_noise(source)
        while True:
            try:
                # Listen for audio continuously
                audio = r.listen(source)
                # Recognize speech
                print("Recognizing...")
                text = r.recognize_google(audio, language='en')
                # Check for a stop command (you can customize this condition)
                if "stop listening" in text.lower():
                    print("Stopping listening...")
                    break
            except sr.UnknownValueError:
                print('Could not understand audio. Please try again.')
    return text
