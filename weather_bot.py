# -*- coding: utf-8 -*-
import requests
import telebot
import config
import random

#TelegramBot
bot = telebot.TeleBot(config.token)

params = dict(q='Kyiv,ua',APPID=config.API_KEY)

res = requests.get(config.url, params=params)
json = res.json()

@bot.message_handler(commands=['wind'])
def mess(message):
    get_message_bot = message.text.strip().lower()
    send_mess = "Ветер " + str(json["wind"]["speed"]) + "м.с. Угол " + str(json["wind"]["deg"])
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('wind', 'temp')
    keyboard.row('oracle')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'wind':
        send_mess = "Ветер " + str(json["wind"]["speed"]) + "м.с. Угол " + str(json["wind"]["deg"])
    elif message.text == 'temp':
        send_mess = "Температура " + str(int(json["main"]["temp"]) - 273)
    elif message.text == 'oracle':
        send_mess = random.choice(open("/home/ros/bot/oracle").readlines())
    bot.send_message(message.chat.id, send_mess, parse_mode='html')

bot.polling(none_stop=True)