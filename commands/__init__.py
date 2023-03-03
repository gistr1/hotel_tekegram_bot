from . import (bestdeal, help, highprice, history, lowprice, start)

from loader import bot

from main import text_message


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text_message = message.text
    print(text_message)
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id,
                         "Привет, {user}! Чем я могу тебе помочь?\n".format(user=message.from_user.first_name, ))
        start.get_start(message)

    else:
        bot.send_message(message.from_user.id,
                         "{user}, я тебя не понял, попробуй /start!\n".format(user=message.from_user.first_name, ))

