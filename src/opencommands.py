import os
import re
import subprocess 
import telegram
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