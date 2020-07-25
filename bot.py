#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import main
import time
import os

#@cfdata_bot
token = open("bot_data.txt", "r").readline()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, напиши мне хэндл, например: kuksag или tourist\n"
                                      "или /info для информации")


@bot.message_handler(commands=['info'])
def start_message(message):
    bot.send_message(message.chat.id, "Данный бот создан @kuksag для образовательных целей\n"
                                      "Описание проекта: https://github.com/kuksag/cfdata\n"
                                      "<i>it's not much but it's honest work</i> (c)", parse_mode="html")


@bot.message_handler(content_types=["text"])
def begin_work(message):
    handle = message.text
    if main.check_handle(handle) != 'OK':
        bot.send_message(message.chat.id, main.check_handle(handle))
        return
    name = str(handle) + str(int(time.time()))
    data = main.main(handle, name)
    for i in ["languages", "tags", "verdicts"]:
        bot.send_photo(message.chat.id, open("temp/{}{}.png".format(i, name), 'rb'))
        os.remove("temp/{}{}.png".format(i, name))
        bot.send_message(message.chat.id, main.build_str(data[i]))
    bot.send_message(message.chat.id, "Всего решалось задач: {}\n"
                                      "Всего решено правильно: {}".format(len(data["attempted"]), len(data["solved"])))

bot.polling()
