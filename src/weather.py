from main import jasminResponse
from pyowm import OWM
from constants import OWM_KEY
from locales import _

def sayWeatherConditions(city):
    openWeatherMap = OWM(API_key=OWM_KEY)
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