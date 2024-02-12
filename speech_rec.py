import speech_recognition as sr
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try :
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en')
    except sr.UnknownValueError:
        print('Say that again please')
takeCommand()