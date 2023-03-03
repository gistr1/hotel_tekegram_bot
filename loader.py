import telebot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters

from config import token_to_access

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token_to_access, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))

