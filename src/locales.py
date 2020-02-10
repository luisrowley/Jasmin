import gettext

#                        #
# global language config #
#                        #
LANGUAGE_CONF = 'en'
_ = gettext.gettext

if LANGUAGE_CONF == 'es':
    es = gettext.translation('base', localedir='locales', languages=['es'])
    es.install()