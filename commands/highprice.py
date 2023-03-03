from database.database import logging
from loader import bot


@bot.message_handler(commands=['highprice'])
@logging
def get_highprice(foo_message):
    bot.send_message(foo_message.from_user.id, "Команда /highprice пока в разработке")