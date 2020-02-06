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

from pyowm import OWM
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
from time import strftime

# Method to interpret user voice
def sendCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=1)
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
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def assistant(command):
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        jasminResponse('The Reddit content has been opened for you Sir.')

while True:
    assistant(sendCommand())