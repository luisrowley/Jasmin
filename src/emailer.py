import smtplib
import constants
from main import jasminResponse, sendCommand
from locales import _

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