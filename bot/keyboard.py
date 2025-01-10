from telebot import types

from utils.enum import ExtraButton, MenuButtons


def create_home_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    home_button = types.KeyboardButton(MenuButtons.HOME)  # Home Button
    markup.add(home_button)
    return markup


def immigration_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [
        types.KeyboardButton(ExtraButton.OFFICIAL_SOURCE),
        types.KeyboardButton(ExtraButton.USER_EXPERIENCES),
    ]
    # home_button = types.KeyboardButton(MenuButtons.HOME)
    markup.add(*buttons)
    # markup.add(home_button)
    return markup


def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = [
        types.KeyboardButton(MenuButtons.IMMIGRATION_QUESTION)
    ]
    second_buttons = [
        types.KeyboardButton(MenuButtons.JOB_SEARCH)
    ]
    third_buttons = [
        types.KeyboardButton(MenuButtons.RESUME_REVIEW)
    ]

    fourth_buttons = [
        types.KeyboardButton(MenuButtons.CASH_BALANCE),
        types.KeyboardButton(MenuButtons.INCREASE_CREDIT),
    ]
    fifth_buttons = [
        types.KeyboardButton(MenuButtons.SUPPORT),
        types.KeyboardButton(MenuButtons.LANGUAGE)
    ]

    markup.add(*first_button)
    markup.add(*second_buttons)
    markup.add(*third_buttons)
    markup.add(*fourth_buttons)
    markup.add(*fifth_buttons)
    return markup
