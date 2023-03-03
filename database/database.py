import functools
import os
import sqlite3 as sq
import datetime


def logging(func):
    """
Декортаор, который пишет в telebot.db id, first_name, username, last_name и время сообщения
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapped(foo_message):
        time = datetime.datetime.now()
        log_param = (foo_message.from_user.id, foo_message.from_user.first_name, foo_message.from_user.username,
               foo_message.from_user.last_name, time)
        print('Логирую', log_param)
        path = os.path.join(os.path.dirname(__file__), 'telebot.db')
        print(path)
        with sq.connect(path) as con:
            cur = con.cursor()

            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", log_param)
        return func(foo_message)

    return wrapped
