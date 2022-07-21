import requests
import getweatherdata as gw
from pprint import pprint
from datetime import datetime

headers = gw.headers

class ForecastData:
    pass


def h3_forecast(city):
    id = gw.city_search(city)
    response = requests.get(f"https://api.gismeteo.net/v2/weather/forecast/{id}/?lang=ru&days=2", headers=headers).json()
    response = response["response"]
    pprint(response)
    forcast_data = []

    start_from = 0
    ct = datetime.utcnow()

    for i in response:
        t = datetime.fromisoformat(i["date"]["UTC"])
        if ct < t:
            break
        start_from += 1

    for i in range(start_from, start_from+3, 1):
        fcd = ForecastData()
        fcd.icon = response[i]["icon"]
        fcd.temp_air = response[i]["temperature"]["air"]["C"]
        fcd.local_time = response[i]["date"]["local"][10:16]
        forcast_data.append(fcd)

    return forcast_data