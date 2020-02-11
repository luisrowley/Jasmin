#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written in Python 2.7

import requests
import json
import wikipedia

from constants import greet_list
from urllib2 import urlopen
from src.main import sendCommand, jasminResponse, sendGreetings, sendBye
from src.locales import _
from src.weather import guessWeather
from src.timeteller import tellCurrentTime
from src.emailer import sendEmail
from src.songplayer import playSong
from src.opencommands import openApplication, openTelegram, openReddit, openWebsite

def assistant(command):

    if _('open reddit') in command:
        openReddit(command)
    
    elif _('open website') in command:
        openWebsite(command)
    
    elif _('launch app') in command:
        openApplication(command)

    elif 'telegram' in command:
        openTelegram()

    elif 'email' in command:
        sendEmail()

    elif any(word in command for word in greet_list):
        sendGreetings()

    elif _('current weather') in command:
        guessWeather(command)

    elif _('time') in command:
        tellCurrentTime()

    elif _('lock screen') in command:
        jasminResponse(_('screen was locked!'))

    elif _("who are you") in command:
        jasminResponse(_("I'm Jasmin, your virtual assistant"))

    elif _('shut down') in command:
        sendBye()
    
    elif _('play me a song') in command:
        playSong()

sendGreetings()
# sayWeatherConditions(constants.DEFAULT_CITY)

while True:
    assistant(sendCommand())