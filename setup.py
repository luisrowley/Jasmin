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
import constants
import datetime
import gettext

from pyowm import OWM
from pynput.keyboard import Key, Controller
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
from time import strftime
from gtts import gTTS

#                        #
# global language config #
#                        #
LANGUAGE_CONF = 'en'
_ = gettext.gettext

if LANGUAGE_CONF == 'es':
    es = gettext.translation('base', localedir='locales', languages=['es'])
    es.install()

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
    tts = gTTS(text=audio, lang=LANGUAGE_CONF)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def assistant(command):

    # initializing word lists
    greet_list = ["hello", "hi", "what's up", "wake up", "hey"]

    if _('open reddit') in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        jasminResponse(_('The Reddit content has been opened for you Sir.'))
    
    elif _('open website') in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = url = 'https://www.' + domain
            webbrowser.open(url)
            jasminResponse(domain + _(' has been opened for you Sir.'))
    
    elif _('launch app') in command:
        openApplication(command)

    elif 'telegram' in command:
        telegramProcess = subprocess.Popen("telegram")
        jasminResponse(_('Telegram ready as always.'))
        print 'Telegram Process: ', telegramProcess.pid
        telegramAssistant(telegramProcess)

    elif 'email' in command:
        sendEmail()

    # greetings and bye
    elif any(word in command for word in greet_list):
        sendGreetings()

    elif _('current weather') in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            sayWeatherConditions(city)
        else:
            sayWeatherConditions("Malaga")

    elif _('time') in command:
        tellCurrentTime()

    elif _('lock screen') in command:
        jasminResponse(_('screen was locked!'))

    elif _("who are you") in command:
        jasminResponse(_("I'm Jasmin, your virtual assistant"))

    elif _('shut down') in command:
        bye_responses = [_("Bye Sir. Have a nice day"), 
                         _("Until next time Sir"), 
                         _("Be nice, bye Sir!")]
        jasminResponse(random.choice(bye_responses))
        sys.exit()

def sayWeatherConditions(city):
    openWeatherMap = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
    observation = openWeatherMap.weather_at_place(city)
    weather = observation.get_weather()
    status = weather.get_status()
    temperature = weather.get_temperature(unit='celsius')
    response = _("Current weather in %(city)s is %(status)s. The maximum temperature is %(temp_max)0.1f and the minimum temperature is %(temp_min)0.1f degree celcius") % ({
                  'city': city, 
                  'status': status, 
                  'temp_max': temperature['temp_max'], 
                  'temp_min': temperature['temp_min']
                  })
    jasminResponse(response)

def tellCurrentTime():
    now = datetime.datetime.now()
    jasminResponse(_('Current time is %(hour)d hours %(mins)d minutes') % ({'hour': now.hour, 'mins': now.minute}))

# function used to open system applications
def openApplication(input):

    if 'google chrome' in input:
        os.system('google-chrome')
        jasminResponse(_('Google Chrome was open for you Sir.'))
    elif 'launch app' in input:
        reg_ex = re.search('launch app (.*)', input)
        if reg_ex:
            appname = reg_ex.group(1)
            subprocess.Popen(appname)     
        jasminResponse(_('I have launched the desired application'))

# telegram voice commands
def telegramAssistant(telegramProcess):

    telegramCommand = sendCommand()

    if 'kill telegram' in telegramCommand:
        telegramProcess.kill()
        jasminResponse(_('Closing Telegram Sir.'))
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
    jasminResponse(_('Who is the recipient?'))
    recipient = sendCommand()
    if 'myself' in recipient:
        jasminResponse(_('What should I say to him?'))
        body = sendCommand()
        jasminResponse(_('What is the subject?'))
        subject = sendCommand()
        content = 'Subject: {}\n\n{}'.format(subject,body)

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(constants.EMAIL_ADDR, constants.EMAIL_SECRET)
        mail.sendmail(constants.EMAIL_ADDR, constants.EMAIL_RECIPIENT, content)
        mail.close()
        jasminResponse(_("Email has been sent successfully."))
    else:
        jasminResponse(_("I don't know what you mean!"))

def sendGreetings():
    day_time = int(strftime('%H'))
    if day_time < 12:
        jasminResponse(_('Hello Sir. Good morning'))
    elif 12 <= day_time < 20:
        jasminResponse(_('Hello Sir. Good afternoon'))
    else:
        jasminResponse(_('Hello Sir. Good evening'))

sendGreetings()
# sayWeatherConditions(constants.DEFAULT_CITY)

while True:
    assistant(sendCommand())