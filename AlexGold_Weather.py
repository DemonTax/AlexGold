import telebot
from telebot import types
import os
import random
from background import keep_alive  # импорт функции для поддержки работоспособности
import pip
import json
import urllib.parse
import urllib.request
import re
from config import API_TOKEN, WEATHER_API_KEY

pip.main(['install', 'pytelegrambotapi'])
import time
import math

bot = telebot.TeleBot(API_TOKEN)

bot_username = "@AlexGold777_bot"

a_de = ['де', "де ты", "а ты де"]
mddt = ['мддт', 'mddt']
hello = ['hi', 'hello', 'prviet', 'привет', 'шалом']
ivan = ['ivan', 'иван', 'ивашка', 'иванушка', 'pidar']
a_sho = ['шо']
dog_answer = ['А шо', 'Шо ты хочешь', 'Я тут мой господин', 'Нахуй ты менэ тегаешь підошва', 'Видьебысь',
              'Я тебя уроню об землю', 'Уебу битой по голови тэбэ']
voice = ['Текстом пиши мразіна дирява', "Я тебе обісцу за таке", 'Ну шо ж ти за гандон', 'Не можу слухать відправ войс',
         "Я на тебе Русіка натравлю, хай він тебе в с сраку виєбе"]
golos = ['голос', 'пес', 'лс', 'voice', 'ls', 'мразь']


def get_random_audio_file():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    audio_files = [file for file in os.listdir(current_directory) if file.endswith('.ogg')]
    random_file = random.choice(audio_files)
    return random_file


def fibonacci(n):
    phi = (1 + math.sqrt(5)) / 2
    psi = (1 - math.sqrt(5)) / 2
    return int((phi ** n - psi ** n) / math.sqrt(5))


def tribonacci(n, memo={}):
    if n in memo:
        return memo[n]
    elif n == 0:
        return 0
    elif n <= 2:
        return 1
    else:
        result = tribonacci(n - 1, memo) + tribonacci(n - 2, memo) + tribonacci(n - 3, memo)
        memo[n] = result
        return result


@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    website = types.KeyboardButton('веб сайт')
    start = types.KeyboardButton('Start')
    markup.add(website, start)
    bot.send_message(message.chat.id, 'Ось гимно якэ ты шукав', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(messege):
    mess = f'{messege.from_user.first_name}, Я тебя уроню об землю'
    bot.send_message(messege.chat.id, mess, parse_mode='html')
    # bot.send_message(messege.chat.id, mess1, parse_mode='html')


@bot.message_handler(commands=['vin'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('ЦЕ котлета', url="https://www.copart.com/"))
    bot.send_message(message.chat.id, 'Ось гимно якэ ты шукав', reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text and "@" + bot.get_me().username in message.text and not message.reply_to_message)
def get_dog(message):
    if message.text.startswith(bot_username):
        bot.reply_to(message, f"{message.from_user.first_name}, {random.choice(dog_answer)}🤡🤡🤡🤡🤡🤡")


@bot.message_handler(func=lambda
        message: message.reply_to_message and message.reply_to_message.from_user.username == bot.get_me().username,
                     content_types=['text'])
def get_user_text(message):
    message_id = message.message_id
    words = message.text.lower().split()
    for word in words:
        if word in a_de:
            audio = open('Я вєздє.ogg', 'rb')
            bot.send_audio(message.chat.id, audio, reply_to_message_id=message_id)
            break
        elif word in a_sho:
            audio = open('Хуй в ушо блядь, мразота.ogg', 'rb')
            bot.send_audio(message.chat.id, audio, reply_to_message_id=message_id)
            break
        elif word.isdigit():
            number = int(word)
            fib_number = fibonacci(number)
            fact = math.factorial(number)
            trib_number = tribonacci(number)
            response = f"""Число Фибоначчи для {number} равно {fib_number},
            Число Трибоначи для {number}  равно {trib_number}
            Факториал для {number} равно {fact},
            Больше я нихуя не знаю, я просто тупой бот AlexGold."""
            bot.send_message(message.chat.id, response)
            break
        elif word in ivan:
            bot.reply_to(message, "Привет, Я Бот AlexGold Дырявэ очко", parse_mode='html')
            break
        elif word in golos:
            bot.send_message(message.chat.id, f"{message.from_user.first_name}, відправив в лс", parse_mode='html')
            audio_file = get_random_audio_file()
            audio = open(audio_file, 'rb')
            bot.send_voice(str(message.from_user.id), audio)
            break
        elif word == 'id':
            bot.send_message(message.chat.id, f'Твой АЙДИ: {message.from_user.id}', parse_mode='html')
            break
        elif word in hello:
            bot.reply_to(message, f'Шалом {message.from_user.username} {message.from_user.first_name} ',
                         parse_mode='html')
            break
        elif word in mddt:
            audio = open('mddt.ogg', 'rb')
            bot.send_audio(message.chat.id, audio, reply_to_message_id=message_id)
            break
    else:
        city = extract_city_from_message(message.text.lower())
        if city:
            weather_data = get_weather(city)
            if weather_data:
                temperature = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                response = f'{message.from_user.first_name} погода в {city}: {description}, Температура: {temperature}°C'
                if temperature > 20:
                    response = f"{message.from_user.first_name} погода в {city}: {description}, Температура: {temperature}°C, Можно ехать мразувать, будуть огненные покосы"
            else:
                response = "Ну ты шо прибитий? Не можешь назву миста без помилок написать?"
            bot.reply_to(message, response)
        else:
            audio_file = get_random_audio_file()
            audio = open(audio_file, 'rb')
            bot.send_audio(message.chat.id, audio, reply_to_message_id=message_id)



def extract_city_from_message(text):
    pattern = r"(?:какая\s+сегодня\s+)?погода(?:\s+в)?(?:\s+в)?\s+([А-Яа-яЁё]+(?:\s+[А-Яа-яЁё]+)*)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).capitalize() if match else None

def get_weather(city):
    encoded_city = urllib.parse.quote(city)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={encoded_city}&lang=ru&appid={WEATHER_API_KEY}&units=metric"
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError:
        return None


@bot.message_handler(func=lambda
        message: message.reply_to_message and message.reply_to_message.from_user.username == bot.get_me().username,
                     content_types=['sticker'])
def get_user_sticker(message):
    """ответ рандом войсом на стикер от юзера"""
    message_id = message.message_id
    audio_file = get_random_audio_file()
    audio = open(audio_file, 'rb')
    bot.send_audio(message.chat.id, audio, reply_to_message_id=message_id)


@bot.message_handler(func=lambda
        message: message.reply_to_message and message.reply_to_message.from_user.username == bot.get_me().username,
                     content_types=['voice'])
def get_user_voice(message):
    """ответ рандом войсом на войс юзера"""
    bot.reply_to(message, f"{message.from_user.first_name}, {random.choice(voice)}")


#     return len(message.photo)


# @bot.message_handler()
# def send_foto(message):
#     if get_user_photo(message) > 1:
#         bot.reply_to(message, f"{random.choice(dog_answer)}, {message.from_user.first_name}")

keep_alive()  # запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0)


print('Hello')