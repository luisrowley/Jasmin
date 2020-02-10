import speech_recognition as sr
from gtts import gTTS
import playsound
import locales

# Method to interpret user voice
def sendCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    # If unrecognizable speech received, callback
    except sr.UnknownValueError:
        print('....')
        command = sendCommand()
    return command

# Convert text to speech
def jasminResponse(audio):
    "speaks audio passed as argument"
    print(audio + '\n')
    tts = gTTS(text=audio, lang=locales.LANGUAGE_CONF)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)