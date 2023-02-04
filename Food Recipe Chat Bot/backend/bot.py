import speech_recognition as sr
from gtts import gTTS
import pyttsx3, os

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)


def engine_talk(text):
    # define variables
    file = "backend/file.mp3"

    # initialize tts, create mp3 and play
    tts = gTTS(text, lang='en', tld="com")
    tts.save(file)
    os.system("mpg123 " + file)


def ask(text, options=None):

    if options:
        for i, j in enumerate(options):
            engine_talk(f"{i+1}. {j}")
    command = user_commands(text)
    return command


def user_commands(text=""):
    try:
        if text:
            engine_talk(text)
        with sr.Microphone() as source:
            command = ""
            
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language="en-US")
            print(command)
            try:
                command = command.lower()
            except:
                pass

            if 'bye' in command:
                print("Bye exitting")
                return 0
            return command
    except Exception as e:
        print(e)
        return 0
