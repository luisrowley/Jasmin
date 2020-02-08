#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written in Python 2.7

import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess 
import youtube_dl
import vlc
import urllib
import urllib2
import json
import wikipedia
import random
import time
import playsound

from pyowm import OWM
from pynput.keyboard import Key, Controller
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
from time import strftime
from gtts import gTTS

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
    print(audio)
    tts = gTTS(text=audio, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def assistant(command):

    # initializing word lists
    greet_list = ["hello", "hi", "what's up", "wake up", "hey"]
    greet_responses = []

    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        jasminResponse('The Reddit content has been opened for you Sir.')
    
    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = url = 'https://www.' + domain
            webbrowser.open(url)
            jasminResponse(domain + ' has been opened for you Sir.')
    
    elif 'launch app' in command:
        openApplication(command)

    elif 'telegram' in command:
        telegramProcess = subprocess.Popen("telegram")
        jasminResponse('Telegram ready as always.')
        print 'Telegram Process: ', telegramProcess.pid
        telegramAssistant(telegramProcess)

    elif 'email' in command:
        sendEmail()

    # greetings and bye
    elif any(word in command for word in greet_list):
        day_time = int(strftime('%H'))
        if day_time < 12:
            jasminResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 20:
            jasminResponse('Hello Sir. Good afternoon')
        else:
            jasminResponse('Hello Sir. Good evening')

    elif 'lock screen' in command:
        jasminResponse('screen was locked!')

    elif 'shut down' in command:
        jasminResponse('Bye Sir. Have a nice day')
        sys.exit()


# function used to open system applications
def openApplication(input):

    if 'google chrome' in input:
        os.system('google-chrome')
        jasminResponse('Google chrome was open for you Sir.')

# telegram voice commands
def telegramAssistant(telegramProcess):

    telegramCommand = sendCommand()

    if 'kill telegram' in telegramCommand:
        telegramProcess.kill()
        jasminResponse('Closing telegram Sir.')
        print 'Telegram Process: ', telegramProcess.pid

    elif 'open chat' in telegramCommand:
        reg_ex = re.search('open (.*) (.+)', telegramCommand)
        if reg_ex:
            chatName = reg_ex.group(2)
            print(chatName)
            keyboard = Controller()
            keyboard.type(chatName)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(0.8)
            keyboard.press(Key.ctrl_l)
            keyboard.press('f')
            keyboard.release('f')
            keyboard.release(Key.ctrl_l)
            time.sleep(0.5)
            keyboard.press(Key.ctrl_l)
            keyboard.press('a')
            keyboard.release('a')
            keyboard.release(Key.ctrl_l)
    
    if telegramCommand == 'kill telegram':
        return
    else:
        telegramAssistant(telegramProcess)

# handle email sending
def sendEmail():

    jasminResponse('Who is the recipient?')
    recipient = sendCommand()
    if 'tony' in recipient:
        jasminResponse('What should I say to him?')
    else:
        jasminResponse('I don\'t know what you mean!')


while True:
    assistant(sendCommand())