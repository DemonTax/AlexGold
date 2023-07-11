import telebot
import json
import urllib.parse
import urllib.request
import re
from config import API_TOKEN, WEATHER_API_KEY

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['text'])
def handle_message(message):
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
    else:
        response = "Пиши правильно назву миста мерзотнык"
    bot.send_message(message.chat.id, response)

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

if __name__ == "__main__":
    bot.polling(none_stop=True)
