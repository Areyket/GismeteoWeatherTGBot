import requests
import getweatherdata as gw
from pprint import pprint

headers = gw.headers

class ForecastData:
    pass


def h3_forecast(city):
    id = gw.city_search(city)
    response = requests.get(f"https://api.gismeteo.net/v2/weather/forecast/{id}/?lang=ru&days=2", headers=headers).json()
    fcd = ForecastData()
    h3 = response["response"][-9]
    fcd.h3_air_temp = h3["temperature"]["air"]["C"]
    fcd.h3_icon = h3["icon"]
    h6 = response["response"][-8]
    fcd.h6_air_temp = h6["temperature"]["air"]["C"]
    fcd.h6_icon = h6["icon"]
    h9 = response["response"][-7]
    fcd.h9_air_temp = h9["temperature"]["air"]["C"]
    fcd.h9_icon = h9["icon"]
    return fcd