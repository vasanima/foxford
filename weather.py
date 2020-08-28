# Python программа для поиска текущей
# детали погоды любого города
# используя openweathermap api


# импорт необходимых модулей
import requests, json
import telebot
from telebot import types
from datetime import datetime


bot = telebot.TeleBot('1108906002:AAEo7LEmAh16wIkkAMhIx5G5QaAyOKKoiiI')

@bot.message_handler(commands=['start', 'help'])
def main(message):
    bot.send_message(message.chat.id, "В каком городе посмотреть погоду на сегодня?")
    bot.register_next_step_handler(message, get_city_name)


@bot.message_handler(content_types=['text'])

def get_city_name (message):
    # Дать название города
    global city_name
    city_name = message.text


    if get_current_weather != False:
        wind, temperature, current_humidity, current_pressure, icon, weather_description = get_current_weather()
        current_temperature = temperature[0]
        current_temperature_max = temperature[2]
        current_temperature_min = temperature[1]
        # вывести следующие значения
        bot_answer = "Температура (C) = " + str(current_temperature) + \
                     '\n Атмосферное давление (in hPa unit) = ' + str(current_pressure) + \
                     "\n Влажность = " + str(current_humidity) + '%' + "\n " + str(weather_description)
        print(bot_answer)
        bot.send_message(message.chat.id, bot_answer)
        bot.send_photo(message.chat.id, 'http://openweathermap.org/img/wn/' + str(icon) + '@2x.png')
        paste_keyboard(message)

    else:

        bot.send_message(message.chat.id, "Такой город не найден. Попробуйте еще раз.")
        bot.register_next_step_handler(message, get_city_name)

def get_current_weather():  # получаем дату
    global lon, lat, api_key
    # Введите свой ключ API здесь

    # api_key = "Your_API_Key"
    api_key = "49830b81a432b27b6eb70e57b4b8af7e"
    # base_url переменная для хранения URL

    base_url = "http://api.openweathermap.org/data/2.5/weather?"



    # complete_url переменная для хранения
    # полный адрес URL

    # complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    # complete_url ='https://api.openweathermap.org/data/2.5/weather?q=London,uk&appid'
    complete_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=' + api_key + '&lang=ru'
    # получить метод модуля запросов
    # вернуть объект ответа

    response = requests.get(complete_url)

    # json метод объекта ответа
    # преобразовать данные формата json в
    # данные формата питона

    x = response.json()
    print(response)
    print(response.text)
    print(x)
    # Теперь x содержит список вложенных словарей
    # Проверьте, что значение ключа "cod" равно
    # "404", значит город найден иначе,
    # город не найден

    if x["cod"] != "404":
        lon = x["coord"]['lon']
        lat = x["coord"]['lat']
        wind = x['wind']['speed']

        # сохранить значение "main"
        # введите переменную y
        y = x['main']

        # сохранить значение, соответствующее
        # к "временному" ключу y
        current_temperature = int(temp_k_c(y["temp"]))

        current_temperature_min  = int(temp_k_c(y["temp_min"]))
        current_temperature_max = int(temp_k_c(y["temp_max"]))

        temperature = [current_temperature, current_temperature_min, current_temperature_max]
        # сохранить значение, соответствующее
        # к клавише "давления" у
        current_pressure = y["pressure"]

        # сохранить значение, соответствующее

        # к клавише «влажность» у

        current_humidity = y["humidity"]

        # сохранить значение «погода»

        # введите переменную z

        z = x["weather"]

        # сохранить значение, соответствующее
        # к ключу "описание" в
        # 0 индекс z


        weather_description = z[0]["description"]

        icon = z[0]['icon']
        return wind, temperature,current_humidity, current_pressure, icon, weather_description
    else:
        return False




def temp_k_c(temp):
    temp = temp - 273
    return temp

def which_weekday(z):
    name_of_day = ''
    day_type = ''
    if z < 5:
        day_type = 'будний день'
    else:
        day_type = 'выходной'
    if z == 0:
        name_of_day = 'понедельник'
    elif z == 1:
        name_of_day = 'вторник'
    elif z == 2:
        name_of_day = 'среда'
    elif z == 3:
        name_of_day = 'четверг'
    elif z == 4:
        name_of_day = 'пятница'
    elif z == 5:
        name_of_day = 'суббота'
    else:
        name_of_day = 'воскресенье'
    return name_of_day

def get_daily_weather(number_of_day):
    global lon, lat, api_key

    # complete_url переменная для хранения
    # полный адрес URL
    complete_url = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(lat) + '&lon=' + str(lon) + \
                   '&appid=' + str(api_key) + '&lang=ru'
    print(complete_url)
    #complete_url = 'https://api.openweathermap.org/data/2.5/onecall?lat=55.751244&lon=37.618423&appid=49830b81a432b27b6eb70e57b4b8af7e'
    print(complete_url)



    # получить метод модуля запросов
    # вернуть объект ответа


    response = requests.get(complete_url)

    # json метод объекта ответа
    # преобразовать данные формата json в
    # данные формата питона

    x = response.json()


    print(response)
    print(response.text)
    daily = x['daily']

    day = int(daily[number_of_day]['dt'])
    print(x['daily'])
    print(day)

    day_date =datetime.fromtimestamp(day).date()
    day_date_weekday = which_weekday(day_date.weekday())
    print(day_date)
    print(day_date_weekday)

    temp_day = int(temp_k_c(daily[number_of_day]['temp']['day']))
    print(temp_day)
    temp_night = int(temp_k_c(daily[number_of_day]['temp']['night']))
    print(temp_night)
    temp_min = int(temp_k_c(daily[number_of_day]['temp']['min']))
    print(temp_min)
    temp_max = int(temp_k_c(daily[number_of_day]['temp']['max']))
    print(temp_max)
    pressure = daily[number_of_day]['pressure']
    print(pressure)
    humidity = daily[number_of_day]['humidity']
    print(humidity)
    wind_speed = daily[number_of_day]['wind_speed']
    print(wind_speed)
    description = daily[number_of_day]['weather'][0]['description']
    print(description)
    icon = daily[number_of_day]['weather'][0]['icon']
    print(icon)

    print(temp_day,temp_night, temp_min, temp_max, pressure, humidity, wind_speed, description, icon)



    return str(day_date), day_date_weekday, temp_day,temp_night, temp_min, temp_max, pressure, humidity, wind_speed, description, icon



def paste_keyboard(message):

    # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    #bot.send_message(message.chat.id, 'Что еще хотите посмотреть?', reply_markup = keyboard)



    key_min_max = types.InlineKeyboardButton(text='t min/max', callback_data='t min/max')
    key_wind = types.InlineKeyboardButton(text='Ветер', callback_data='wind')
    key_days = types.InlineKeyboardButton(text='Погода на 5 дней', callback_data='days')

    # И добавляем кнопку на экран
    keyboard.add(key_min_max)
    keyboard.add(key_wind)

    keyboard.add(key_days)
    bot.send_message(message.from_user.id, text='Что еще посмотрим?', reply_markup=keyboard)

    print('here')


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    wind, temperature, current_humidity, current_pressure, icon, weather_description = get_current_weather()
    current_temperature = temperature[0]
    current_temperature_max = temperature[2]
    current_temperature_min = temperature[1]

    # Если нажали на одну из кнопок

    if call.data == 't min/max':
        msg = "Минимальная температура (C) = " + str(current_temperature_min) + \
              "\nМаксимальная температура (C) = " + str(current_temperature_max)
        bot.send_message(call.message.chat.id, msg)

    elif call.data == 'wind':
        msg = "Скорость ветра " + str(wind) + 'м/с'
        bot.send_message(call.message.chat.id, msg)

    elif call.data == 'days':
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # bot.send_message(message.chat.id, 'Что еще хотите посмотреть?', reply_markup = keyboard)

        key_full = types.InlineKeyboardButton(text='Полный прогноз', callback_data='full')
        key_short = types.InlineKeyboardButton(text='Краткий прогноз', callback_data='short')

        keyboard.add(key_full)
        keyboard.add(key_short)
        bot.send_message(call.message.chat.id, text='Выберете', reply_markup=keyboard)
    elif call.data == 'full':
        for number_of_day in range(0, 5):
            day_date, day_date_weekday, temp_day, temp_night, temp_min, temp_max, pressure, humidity, wind_speed, description, icon = get_daily_weather(number_of_day)
            bot.send_message(call.message.chat.id,
                             day_date + '\n' + str(day_date_weekday) + '\nТемпература днем ' + str(temp_day) +
                             '\nТемпература ночью ' + str(temp_night) + '\nТемпература min/max '
                             + str(temp_min) + '/' + str(temp_max) + '\nДавление ' + str(pressure)
                             + '\nВлажность ' + str(humidity) + '\nСкорость ветра ' + str(wind_speed) + 'м/с'
                             + '\n' + str(description))

            bot.send_photo(call.message.chat.id, 'http://openweathermap.org/img/wn/' + str(icon) + '@2x.png')

    elif call.data == 'short':
        for number_of_day in range(0, 5):
            day_date, day_date_weekday, temp_day, temp_night, temp_min, temp_max, pressure, humidity, wind_speed, description, icon = get_daily_weather(
                number_of_day)
            bot.send_message(call.message.chat.id, day_date + '\n' + str(day_date_weekday) +
                             '\nТемпература min/max ' + str(temp_min) + '/' + str(temp_max) + '\n' + str(description))

            bot.send_photo(call.message.chat.id, 'http://openweathermap.org/img/wn/' + str(icon) + '@2x.png')


    else:
        msg = "Чтобы повторить, нажмите /start "
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)




bot.polling(none_stop=True)
