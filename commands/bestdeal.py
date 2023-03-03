from database.database import logging
from loader import bot


@bot.message_handler(commands=['bestdeal'])
@logging
def get_bestdeal(foo_message):
    bot.send_message(foo_message.from_user.id, "Команда /bestdeal пока в разработке")