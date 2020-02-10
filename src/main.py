import speech_recognition as sr
from time import strftime
from gtts import gTTS
from locales import _
import playsound
import locales
import random
import sys

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

# basic greeting function
def sendGreetings():
    day_time = int(strftime('%H'))
    if day_time < 12:
        jasminResponse(_('Hello Sir. Good morning'))
    elif 12 <= day_time < 20:
        jasminResponse(_('Hello Sir. Good afternoon'))
    else:
        jasminResponse(_('Hello Sir. Good evening'))

def sendBye():
    bye_responses = [_("Bye Sir. Have a nice day"), 
                         _("Until next time Sir"), 
                         _("Be nice, bye Sir!")]
    jasminResponse(random.choice(bye_responses))
    sys.exit()