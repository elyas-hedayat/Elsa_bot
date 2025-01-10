import telebot

from apis.chat import process_ai_chat_handler
from apis.metis import create_metis_session
from bot.keyboard import audio_keyboard, home_keyboard, immigration_keyboard, menu_keyboard
from config.config import Config
from utils.enum import ExtraButton, MenuButtons, MessageEnum

API_TOKEN = Config.API_TOKEN

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(func=lambda message: message.text == MenuButtons.HOME)
def handle_home_button(message):
    response_text = "منو اصلی"
    bot.send_message(message.chat.id, response_text, reply_markup=menu_keyboard())


@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = MessageEnum.WELCOME
    bot.send_message(message.chat.id, welcome_text, reply_markup=menu_keyboard())


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "🆘 Available commands:\n"
        "/start - Start interacting wSith the bot\n"
        "/help - Get help information"
    )
    bot.reply_to(message, help_text)


@bot.message_handler(func=lambda message: message.text in [
    MenuButtons.IMMIGRATION_QUESTION,
    MenuButtons.JOB_SEARCH,
    MenuButtons.RESUME_REVIEW,
    MenuButtons.CASH_BALANCE,
    MenuButtons.INCREASE_CREDIT,
    MenuButtons.SUPPORT,
    MenuButtons.LANGUAGE,
])
def handle_legal_support_selection(message):
    reply_markup = menu_keyboard()
    if message.text == MenuButtons.IMMIGRATION_QUESTION:
        response_text = MessageEnum.IMMIGRATION_QUESTION
        reply_markup = immigration_keyboard()
    elif message.text == MenuButtons.JOB_SEARCH:
        response_text = MenuButtons.JOB_SEARCH
    elif message.text == MenuButtons.RESUME_REVIEW:
        response_text = MessageEnum.RESUME_RESPONSE
    elif message.text == MenuButtons.CASH_BALANCE:
        response_text = MessageEnum.CASH_BALANCE.format(message.from_user.first_name)
    elif message.text == MenuButtons.INCREASE_CREDIT:
        response_text = MenuButtons.INCREASE_CREDIT
    elif message.text == MenuButtons.SUPPORT:
        response_text = MessageEnum.SUPPORT.format(message.from_user.first_name)
    elif message.text == MenuButtons.LANGUAGE:
        response_text = MessageEnum.LANGUAGE_RESPONSE
    bot.reply_to(message, response_text, reply_markup=reply_markup)


@bot.message_handler(func=lambda message: message.text in [
    ExtraButton.OFFICIAL_SOURCE,
    ExtraButton.USER_EXPERIENCES,
])
def handle_immigration_choice(message):
    if message.text == ExtraButton.OFFICIAL_SOURCE.value:
        response_text = MessageEnum.LEGAL_RESPONSE_BOT
        session_id = create_metis_session(bot_id=Config.BOT_ID)
        bot.register_next_step_handler(message, process_ai_chat, session_id)
    elif message.text == ExtraButton.USER_EXPERIENCES.value:
        response_text = MessageEnum.EXPERIENCE_RESPONSE_BOT
    bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=home_keyboard()
    )


def process_ai_chat(message, session_id):
    if message.text.lower() == "🏠 بازگشت به منو اصلی":
        bot.send_message(
            chat_id=message.chat.id,
            text="منو اصلی",
            reply_markup=home_keyboard()
        )
        return
    ai_response = process_ai_chat_handler(message, session_id)
    reply_markup = audio_keyboard()
    bot.send_message(message.chat.id, ai_response, reply_markup=reply_markup)
    bot.register_next_step_handler(message, process_ai_chat, session_id)


bot.infinity_polling()
