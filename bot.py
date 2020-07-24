#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import main
import time
import os

token = open("bot_data.txt", "r").readline()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, напиши мне хэндл или /help \n"
                                      " (например: kuksag)")


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, "Данный бот создан @kuksag для образовательных целей\n"
                                      "Описание проекта: https://github.com/kuksag/cfdata")


@bot.message_handler(content_types=["text"])
def begin_work(message):
    handle = message.text
    if main.check_handle(handle) != 'OK':
        bot.send_message(message.chat.id, main.check_handle(handle))
        return
    name = str(handle) + str(int(time.time()))
    main.main(handle, name)
    for i in range(3):
        bot.send_photo(message.chat.id, open("temp/{}{}.png".format(i, name), 'rb'))
        os.remove("temp/{}{}.png".format(i, name))


bot.polling()
