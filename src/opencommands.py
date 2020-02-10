import os
import re
import subprocess
import telegram
import webbrowser
from main import jasminResponse
from locales import _

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

def openTelegram():
    telegramProcess = subprocess.Popen("telegram")
    jasminResponse(_('Telegram ready as always.'))
    print 'Telegram Process: ', telegramProcess.pid
    telegram.telegramAssistant(telegramProcess)

def openReddit(command):
    reg_ex = re.search('open reddit (.*)', command)
    url = 'https://www.reddit.com/'
    if reg_ex:
        subreddit = reg_ex.group(1)
        url = url + 'r/' + subreddit
    webbrowser.open(url)
    jasminResponse(_('The Reddit content has been opened for you Sir.'))

def openWebsite(command):
    reg_ex = re.search('open website (.+)', command)
    if reg_ex:
        domain = reg_ex.group(1)
        print(domain)
        url = url = 'https://www.' + domain
        webbrowser.open(url)
        jasminResponse(domain + _(' has been opened for you Sir.'))