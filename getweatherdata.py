import json
import requests
from pprint import pprint

with open("config.json", "r", encoding="utf-8") as config_file:
    data = json.load(config_file)

city = "Москва"
headers = data["headers"]


def city_search(city):
    response = requests.get(f"https://api.gismeteo.net/v2/search/cities/?lang=ru&query={city}", headers=headers).json()
    return response["response"]["items"][0]["id"]


class WeatherData:
    cloudiness, description, humidity, icon, pressure, temp_air, temp_feels, wind_dir, wind_speed = None, None, None, None, None, None, None, None, None


def city_weather(city):
    id = city_search(city)
    response = requests.get(f"https://api.gismeteo.net/v2/weather/current/{id}/?lang=ru", headers=headers).json()
    response = response["response"]
    wd = WeatherData()
    wd.cloudiness = response["cloudiness"]["percent"]
    wd.cloudiness_desc = response["cloudiness"]["type"]
    wd.description = response["description"]["full"]
    wd.humidity = response["humidity"]["percent"]
    wd.icon = response["icon"]
    wd.pressure = response["pressure"]["mm_hg_atm"]
    wd.temp_air = response["temperature"]["air"]["C"]
    wd.temp_feels = response["temperature"]["comfort"]["C"]
    wd.wind_dir = response["wind"]["direction"]["scale_8"]
    wd.wind_speed = response["wind"]["speed"]["m_s"]
    wd.temp_water = response["temperature"]["water"]["C"]

    return wd


pprint(city_weather(city).icon)