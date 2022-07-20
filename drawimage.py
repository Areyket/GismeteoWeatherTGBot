from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import getweatherdata as gw
import h3_forecast as fc
import cairosvg
import math

now = datetime.now()
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
wind_dic = ["Штиль", "Северный", "Северо-восточный", "Восточный", "Юго-восточный", "Южный", "Юго-западный", "Западный", "Северо-западный"]
cloud_dic = ["Ясно", "Малооблачно", "Облачно", "Пасмурно", "Переменная облачность"]

today = now.day
weekday = datetime.today().weekday()
month = now.month

current_time = now.strftime("%H:%M")

WEIGHT, HEIGHT = (1080, 1080)  # Удалить?


def set_font(font, scale):  # Устанавливаем размер
    done_font = ImageFont.truetype(f"fonts/{font}.otf", size=scale)
    return done_font

weather = gw.city_weather("Москва")
forecast = fc.h3_forecast("Москва")
# weather = gw.WeatherData()
# weather.temp_feels = 25
# weather.temp_air = 25
# weather.description = "Небольшой дождь"
# weather.icon = "c3_r1"
# weather.humidity = "90"
# weather.wind_speed = 4.2
# weather.wind_dir = 2
wind_word = wind_dic[weather.wind_dir]
# weather.pressure = 750
# weather.cloudiness = 20
# weather.temp_water = 20
# weather.cloudiness_desc = 2
cloud_word = cloud_dic[weather.cloudiness_desc]

weather.temp_air = "+" + str(weather.temp_air) if weather.temp_air > 0 else weather.temp_air
weather.temp_feels = "+" + str(weather.temp_feels) if weather.temp_feels > 0 else weather.temp_feels
weather.temp_water = "+" + str(weather.temp_water) if weather.temp_water > 0 else weather.temp_water

img = Image.open("test.png").convert("RGBA")  # Открываем картинку


draw = ImageDraw.Draw(img)

center = WEIGHT / 2
width_of_temp_text = int((set_font("reg", 96).getlength(f"{weather.temp_air} °")))
width_of_temp_row = width_of_temp_text + 100
start_point = (center - width_of_temp_row / 2) - 10

# topsite
draw.text((540, 80), "Москва", anchor="mt", font=set_font("reg", 48))
draw.text((540, 130), "Сейчас", anchor="mt", font=set_font("reg", 24))
draw.text((50, 75), current_time, font=set_font("reg", 24))
draw.text((50, 110), f"{today} {months[month]}", font=set_font("thin", 18))
draw.text((50, 130), f"{days[weekday]}", font=set_font("thin", 18))

# middle
draw.text((start_point, 340), f"{weather.temp_air} °", anchor="la", font=set_font("reg", 96))
draw.text((540, 450), f"{weather.description}", anchor="mt", font=set_font("reg", 36))
draw.text((540, 500), f"Ощущается как: {weather.temp_feels} °", anchor="mt", font=set_font("thin", 24))

# bottom
cairosvg.svg2png(url=f"images/new/{weather.icon}.svg", write_to="tmp/tmp.png", output_width=100, output_height=100)
img_to_combine = Image.open(f"tmp/tmp.png", "r").convert("RGBA")
# img.alpha_composite(img_to_combine, (540 + int((set_font("reg", 48).getlength(f"{weather.temp_air} °"))), 340))
img.alpha_composite(img_to_combine, (int(start_point + width_of_temp_row - 90), 340))
# draw.rectangle([(start_point, 350), (start_point+10, 360)], 0xFF0000FF)

# left humidity
cairosvg.svg2png(url=f"svg/hum.svg", write_to="tmp/hum.png", output_width=50, output_height=50)
img_to_combine = Image.open(f"tmp/hum.png", "r").convert("RGBA")
img.alpha_composite(img_to_combine, (50, 620))
draw.text((115, 615), f"{weather.humidity} %", font=set_font("reg", 48))

# left wind
cairosvg.svg2png(url=f"svg/wind.svg", write_to="tmp/wind.png", output_width=50, output_height=50)
img_to_combine = Image.open(f"tmp/wind.png", "r").convert("RGBA")
img.alpha_composite(img_to_combine, (50, 700))
draw.text((115, 695), f"{weather.wind_speed} м/с", font=set_font("reg", 48))
draw.text((115, 750), f"{wind_word}", font=set_font("reg", 18))

# left pressure
cairosvg.svg2png(url=f"svg/pressure.svg", write_to="tmp/pressure.png", output_width=50, output_height=50)
img_to_combine = Image.open(f"tmp/pressure.png", "r").convert("RGBA")
img.alpha_composite(img_to_combine, (50, 800))
draw.text((115, 795), f"{weather.pressure} мм. рт. ст.", font=set_font("reg", 48))

#left cloudiness
cairosvg.svg2png(url=f"svg/cloud.svg", write_to="tmp/cloud.png", output_width=50, output_height=50)
img_to_combine = Image.open(f"tmp/cloud.png", "r").convert("RGBA")
img.alpha_composite(img_to_combine, (50, 880))
draw.text((115, 875), f"{weather.cloudiness} %", font=set_font("reg", 48))
draw.text((115, 930), f"{cloud_word}", font=set_font("reg", 18))

#left water
cairosvg.svg2png(url=f"svg/water.svg", write_to="tmp/water.png", output_width=50, output_height=50)
img_to_combine = Image.open(f"tmp/water.png", "r").convert("RGBA")
img.alpha_composite(img_to_combine, (50, 970))
draw.text((115, 965), f"{weather.temp_water} °", font=set_font("reg", 48))


print(forecast.h3_icon)

img.save("test_text.png")