from main import sendCommand, jasminResponse
from pynput.keyboard import Key, Controller
from locales import _
import time
import re

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