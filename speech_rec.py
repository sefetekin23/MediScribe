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
                audio = r.listen(source, timeout=2)  # Adjust timeout as needed
                # Recognize speech
                print("Recognizing...")
                input = r.recognize_google(audio, language='en')
                # Check for a stop command (you can customize this condition)
                if "stop listening" in input.lower():
                    print("Stopping listening...")
                    break
            except sr.UnknownValueError:
                print('Could not understand audio. Please try again.')
    return input

if __name__ == "__main__":
    result = take_input()
    print("You said:", result)

test_speech = ''' I have had a cough for the past week. 
It’s kind of chesty and i feel breathless when it happens. 
I am taking some paracetamol. 
You have a respiratory infection. 
You should do a physical exam. '''