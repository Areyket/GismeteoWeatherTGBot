import json
import drawimage as di
import getweatherdata as gd
from geopy.geocoders import Nominatim
from pprint import pprint

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


with open("config.json", "r", encoding="utf-8") as config_file:
    data = json.load(config_file)

API_TOKEN = data["token"]["token"]
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    cities = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    cities.add(KeyboardButton("Отправить геолокацию 📍", request_location=True))
    cities.add(KeyboardButton("Москва"), KeyboardButton("Санкт-Петербург"), KeyboardButton("Сургут"),
               KeyboardButton("Нижний-Тагил"), KeyboardButton("Йошкар-Ола"), KeyboardButton("Лион"))
    msg = bot.send_message(message.chat.id, "Привет! Напишите название населенного пункта или отправь свою геолокацию, чтобы я "
                                            "показал тебе погоду:", reply_markup=cities)


def process_send_weather(message, city):
    di.draw_image(city)
    weather_image_done = open('tmp/w_image.png', 'rb')
    bot.send_photo(message.chat.id, weather_image_done)


@bot.message_handler()
def handle_message(message):
    msg = bot.send_message(message.chat.id, "Думаю...")
    process_send_weather(message, message.text)
    bot.delete_message(msg.chat.id, msg.id)


@bot.message_handler(content_types=['location'])
def handle_loc(message):
    # print(message.location)
    # user_geo_long, user_geo_lat = message.location.longitude, message.location.latitude
    # print(user_geo_long, user_geo_lat)
    # geolocator = Nominatim(user_agent="geoapiExercises")
    # location = geolocator.reverse(str(user_geo_lat) + "," + str(user_geo_long), zoom=5)
    # location_final = location.raw["address"]["state"]
    # process_send_weather(message, location_final)
    pass


def process_city_send(message):
    msg = bot.send_message(message.chat.id, "Думаю...")
    process_send_weather(message, message.text)
    bot.delete_message(msg.chat.id, msg.id)
    # if message.location:
    #     handle_loc(message)
    #     return
    # if (message.text) != "Ошибка местоположения":
    #     process_send_weather(message, message.text)
    # else:
    #     bot.send_message(message.chat.id, "Ошибка местоположения!")


# @bot.message_handler(commands=['weather'])
# def weather_command_message(message):
#     cities = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
#     cities.add(KeyboardButton("Отправить геолокацию 📍", request_location=True))
#     cities.add(KeyboardButton("Москва"), KeyboardButton("Санкт-Петербург"), KeyboardButton("Сургут"),  KeyboardButton("Нижний-Тагил"), KeyboardButton("Йошкар-Ола"),  KeyboardButton("Лион"))
#     cities.add(KeyboardButton("Назад"))
#     msg = bot.send_message(message.chat.id, "Напишите название населенного пункта или отправь свою геолокацию, чтобы я "
#                                       "показал тебе погоду:", reply_markup=cities)
#
#     bot.register_next_step_handler(msg, process_city_send)


bot.infinity_polling()