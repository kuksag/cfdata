#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import main

# @cfdata_bot
token = open("bot_data.txt", "r").readline()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, напиши мне хэндл, например: kuksag или tourist\n"
                                      "\n/info для информации")


@bot.message_handler(commands=['info'])
def start_message(message):
    bot.send_message(message.chat.id, "Данный бот создан @kuksag для образовательных целей\n"
                                      "Описание проекта: https://github.com/kuksag/cfdata\n"
                                      "<i>it's not much but it's honest work</i> (c)", parse_mode="html")


@bot.message_handler(content_types=["text"])
def begin_work(message):
    handle = message.text
    user = main.User(handle)

    if user.profile is None:
        bot.send_message(chat_id=message.chat.id, text='Хэндл "{}" не найден'.format(handle))
        return
    if not user.build():
        print("Что-то не так")
        return

    bot.send_photo(chat_id=message.chat.id,
                   photo=main.draw_pie(user.languages, figure_name="Статистика по языкам программирования",
                                       legend_name="Языки программирования"),
                   caption=main.build_str(main.sort_dict(user.languages)))
    bot.send_photo(chat_id=message.chat.id,
                   photo=main.draw_pie(user.tags, figure_name="Статистика по задачам",
                                       legend_name="Тэги"),
                   caption=main.build_str(main.sort_dict(user.tags)))
    bot.send_photo(chat_id=message.chat.id,
                   photo=main.draw_pie(user.verdicts, figure_name="Статистика по вердиктам",
                                       legend_name="Вердикты"),
                   caption=main.build_str(main.sort_dict(user.verdicts)))
    bot.send_message(chat_id=message.chat.id,
                     text="Всего решалось задач: {}\nВсего решено правильно: {}".format(len(user.attempted),
                                                                                        len(user.solved)))


bot.polling()
