from database.database import logging
from loader import bot


@bot.message_handler(commands=['history'])
@logging
def get_history(foo_message):
    bot.send_message(foo_message.from_user.id, "Команда /history пока в разработке")