import functools
import logging
import datetime

import telebot
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

from telebot.types import ReplyKeyboardRemove, CallbackQuery
from telebot.handler_backends import State, StatesGroup  # States

from loader import bot


# logger = telebot.logger # узнать для чего это
# telebot.logger.setLevel(logging.DEBUG)


class MyState(StatesGroup):
    city = State()
    count_hotel = State()
    photo = State()
    check_in = State()
    check_out = State()

# Creates a unique calendar
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")

calendar_2 = Calendar(language=RUSSIAN_LANGUAGE)
calendar_2_callback = CallbackData("calendar_2", "action", "year", "month", "day")

user_dates = dict()


@bot.message_handler(state=MyState.check_in)
def select_from_calenar_check_in(message):
    """
    Catches a message with the command "start" and sends the calendar
    :param message:
    :return:
    """

    now = datetime.datetime.now()  # Get the current date
    bot.send_message(
        message.chat.id,
        "Выберет пожалуйста дату заезда",
        reply_markup=calendar.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.

    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Ваша дата заезда {date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        checkindate = date.strftime('%d.%m.%Y')
        print(f"{calendar_1_callback}: Day: {checkindate}")
        user_dates[call.from_user.id] = {'checkindate': checkindate}
        print('Записал в словарь дату заезда', user_dates)
        bot.set_state(call.from_user.id, MyState.check_out, call.from_user.id)
        select_from_calenar_check_out(call.message)

    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_callback}: Cancellation")


@bot.message_handler(state=MyState.check_out)
def select_from_calenar_check_out(message):
    """
    Catches a message with the command "start" and sends the calendar
    :param message:
    :return:
    """

    now = datetime.datetime.now()  # Get the current date
    bot.send_message(
        message.chat.id,
        "Выберете дату выезда",
        reply_markup=calendar_2.create_calendar(
            name=calendar_2_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_2_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_2_callback.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar_2.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.

    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Ваша дата выезда {date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        checkoutdate = date.strftime('%d.%m.%Y')
        print(f"{calendar_2_callback}: Day: {checkoutdate}")
        user_dates[call.from_user.id].update({'checkoutdate': checkoutdate})
        print('Записал в словарь дату выезда', user_dates)

        bot.send_message(call.from_user.id, 'Сколько отелей выводить?')
        bot.set_state(call.from_user.id, MyState.count_hotel, call.from_user.id)


    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_2_callback}: Cancellation")
