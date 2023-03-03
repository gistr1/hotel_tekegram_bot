from telebot import types

from commands import lowprice, highprice, bestdeal, history, help
from database.database import logging

from loader import bot
from config import list_commands


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    data = {
        'start': get_start,
        'lowprice': lowprice.get_lowprice,
        'highprice': highprice.get_highprice,
        'bestdeal': bestdeal.get_bestdeal,
        'history': history.get_history,
        'help': help.get_help
    }
    data[call.data](call)



@bot.message_handler(commands=['start'])
@logging
def get_start(foo_message):

    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    for command in list_commands:
        keyboard.add(types.InlineKeyboardButton(text='/{command}'.format(command=command),
                                                callback_data='{command}'.format(command=command)))

    bot.send_message(foo_message.from_user.id, text='Перечень доступных команд:', reply_markup=keyboard)
