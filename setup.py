#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written in Python 2.7

import re
import webbrowser
import requests
import youtube_dl
import vlc
import urllib
import urllib2
import json
import wikipedia

from constants import greet_list
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
from src.main import sendCommand, jasminResponse, sendGreetings, sendBye
from src.locales import _
from src.weather import sayWeatherConditions
from src.timeteller import tellCurrentTime
from src.emailer import sendEmail
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
        sendBye()

sendGreetings()
# sayWeatherConditions(constants.DEFAULT_CITY)

while True:
    assistant(sendCommand())