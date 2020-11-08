import telebot
from telebot import types
import config
import str_data
from peewee import *

db = SqliteDatabase('med.db')

class Pacients(Model):
    first_name = CharField()
    last_name = CharField()
    chat_id = IntegerField()

    class Meta:
        database = db

Pacients.create_table()

def kbd_main():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for btn in str_data.btns_main:
        keyboard.add(btn)
    return keyboard

def kbd_head():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for key, value in str_data.kbd_head.items():
        keyboard.add(types.InlineKeyboardButton(value, callback_data=key))
    return keyboard

bot = telebot.TeleBot(config.token, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_start(message):
    try:
        print(Pacients.get(Pacients.chat_id == message.chat.id))
    except IndexError or SQL:
        new_pacient = Pacients(first_name = str(message.chat.first_name), last_name = str(message.chat.last_name), chat_id = message.chat.id)
        new_pacient.save()
        print("Новый пациент добавлен")
    bot.send_message(message.chat.id, str_data.startText, reply_markup=kbd_head())

@bot.message_handler(content_types=['text'])
def send_text(message):
    cAns = False
    for i in range(len(str_data.answ_main)):
        if message.text == str_data.btns_main[i]:
            bot.send_message(message.chat.id, str_data.answ_main[i], reply_markup=kbd_main())
            cAns = True
    if cAns == False:
        bot.send_message(message.chat.id, (Pacients.get(Pacients.chat_id == message.chat.id)).first_name+", бот вас не понял")

@bot.callback_query_handler(func=lambda call:True)
def answer_head(call):
    if call.data == "zatilok":
        bot.send_message(call.from_user.id, "У вас проблемы с затылком")
    if call.data == "glaza":
        bot.send_message(call.from_user.id, "У вас проблемы с глазами")
    if call.data == "viski":
        bot.send_message(call.from_user.id, "У вас проблемы с висками")
    if call.data == "lob":
        bot.send_message(call.from_user.id, "У вас проблемы со лбом")
    if call.data == "otst":
        bot.send_message(call.from_user.id, "У вас проблем нет")


bot.polling()