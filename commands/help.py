from telebot import types

from database.database import logging
from loader import bot
from config import list_commands


@bot.message_handler(commands=['help'])
@logging
def get_help(foo_message):
    print(foo_message)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # наша клавиатура
    for command in list_commands:
        keyboard.add(types.KeyboardButton(text='/{command}'.format(command=command)))
    bot.send_message(foo_message.from_user.id, text='Перечень доступных команд:', reply_markup=keyboard)
