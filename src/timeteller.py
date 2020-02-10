import datetime
from main import jasminResponse
from locales import _

def tellCurrentTime():
    now = datetime.datetime.now()
    jasminResponse(_('Current time is %(hour)d hours %(mins)d minutes') % ({'hour': now.hour, 'mins': now.minute}))
