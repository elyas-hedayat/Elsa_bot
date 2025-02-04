import json
import random
import re

import requests
import telebot
from gtts import gTTS
from jobspy import scrape_jobs
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apis.chat import process_ai_chat_handler
from apis.metis import create_metis_session
from bot.keyboard import audio_keyboard, home_keyboard, immigration_keyboard, menu_keyboard
from config.config import Config
from config.redis_conf import redis_client
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
        response_text = MessageEnum.JOB_SEARCH
        bot.register_next_step_handler(message, process_job_search)
    elif message.text == MenuButtons.RESUME_REVIEW:
        response_text = MessageEnum.RESUME_RESPONSE
    elif message.text == MenuButtons.CASH_BALANCE:
        response_text = MessageEnum.CASH_BALANCE.format(message.from_user.first_name)
    elif message.text == MenuButtons.INCREASE_CREDIT:
        response_text = MessageEnum.INCREASE_CREDIT
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
        session_id = create_metis_session(bot_id=Config.EXPERIENCE_CHAT_ID)
        response_text = MessageEnum.EXPERIENCE_RESPONSE_BOT
        bot.register_next_step_handler(message, process_ai_experience_chat, session_id)
    bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=home_keyboard()
    )


def process_ai_chat(message, session_id):
    if message.text.lower() == MenuButtons.HOME:
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.send_message(
            chat_id=message.chat.id,
            text="منو اصلی",
            reply_markup=menu_keyboard()
        )
        return
    ai_response = process_ai_chat_handler(message.text, session_id)
    reply_markup = audio_keyboard()
    bot.send_message(message.chat.id, ai_response, reply_markup=reply_markup)
    bot.register_next_step_handler(message, process_ai_chat, session_id)


def process_ai_experience_chat(message, session_id):
    if message.text.lower() == MenuButtons.HOME:
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.send_message(
            chat_id=message.chat.id,
            text="منو اصلی",
            reply_markup=menu_keyboard()
        )
        return
    ai_response = process_ai_chat_handler(message.text, session_id)
    reply_markup = audio_keyboard()
    bot.send_message(message.chat.id, ai_response, reply_markup=reply_markup)
    bot.register_next_step_handler(message, process_ai_experience_chat, session_id)


@bot.callback_query_handler(func=lambda call: call.data == "Audio")
def handle_audio_request(call):
    try:
        name = f"f{random.randint(1, 10000000)}.mp3"
        bot.send_message(
            chat_id=call.message.chat.id,
            text="⏳ درحال تولید فایل صوتی... لطفا صبر کنید"
        )
        text = call.message.text
        is_persian = any('\u0600' <= c <= '\u06FF' for c in text)
        lang = 'fa' if is_persian else 'en'
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(name)

        # Send the audio file back to the user
        with open(name, 'rb') as audio:
            bot.send_audio(chat_id=call.message.chat.id, audio=audio)
    except Exception:
        error_message = "در حال حاضر فقط متن های انگلیسی به ویس تبدیل میشه.."
        bot.send_message(chat_id=call.message.chat.id, text=error_message)


def process_job_chat(message, session_id):
    if message.text.lower() == 'exit':
        bot.send_message(message.chat.id, "Chat with AI ended.", reply_markup=menu_keyboard())
        return

    url = f'https://api.metisai.ir/api/v1/chat/session/{session_id}/message'
    headers = {
        'Authorization': f'Bearer {Config.METIS_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "message": {
            "content": message.text,
            "type": "USER"
        }
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        ai_response = response.json().get('content', 'No response from AI')
        return ai_response
    else:
        bot.send_message(message.chat.id, "Failed to get response from AI. Please try again.")
    bot.register_next_step_handler(message, process_ai_chat, session_id)


def process_job_search(message):
    try:
        data = create_metis_session(bot_id=Config.JOB_BOT_ID)
        ai_response = process_job_chat(message=message, session_id=data)
        job_info_dict = ai_response.split("python", 1)[1].strip()
        pattern = r'"(job(?:_title|_description|)?|city|country)":\s*"([^"]+)"'
        matches = re.findall(pattern, job_info_dict)
        result = {key: value for key, value in matches}
        job_keys = ["job", "job_title", "job_description"]

        job = next((result[key] for key in job_keys if key in result), None)
        city = result.get("city", None)
        country = result.get("country", None)
        result = {
            "job": job,
            "city": city,
            "country": country
        }
        info_message = \
            f"الان دنبال موقعیت های مربوط به {result.get('job')} توی{result.get('country')} " \
            f"/ {result.get('city')} میگردم "
        bot.send_message(message.chat.id, info_message)
        user_id = str(message.chat.id)
        jobs = scrape_jobs(
            site_name=["google", "linkedin"],
            search_term=result.get("job"),
            google_search_term=
            f"{result.get('job')} jobs near {result.get('country')}, {result.get('city')} yesterday",
            location=f"{result.get('country')}",
            results_wanted=20,
            hours_old=100,
            # country_indeed=result.get('country'),
            # country_indeed='USA',
            # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
            # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
        )

        for index, row in jobs.iterrows():
            print(row)
            job_details = {
                "title": row.get("title", ""),
                "company": row.get("company", ""),
                "job_url": row.get('job_url', ''),
                "company_url": row.get('company_url', ''),
                "site": row.get("site", " "),
                "location": row.get("location", "")
            }
            redis_client.lpush(user_id, json.dumps(job_details))
        send_job(user_id, 0)
    except ValueError:
        bot.send_message(message.chat.id, "یه اتفاقی افتاد که نباید میفتاد دوباره سرچ کن از اول")
        bot.register_next_step_handler(message, process_job_search)


def send_job(user_id, index):
    job_data = redis_client.lrange(user_id, 0, -1)

    print(job_data)
    if 0 <= index < len(job_data):
        job_data = redis_client.lindex(user_id, index)
        print(job_data)
        job_data = json.loads(job_data)

        keyboard = [
            [
                InlineKeyboardButton("🔗 Apply", url=job_data.get('job_url', 'نداره')),
                InlineKeyboardButton("🔗 Company", url=job_data.get('company_url', 'نداره'))

            ],
            [
                InlineKeyboardButton("Next", callback_data=f"next:{index}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        search_summary = (
            f"💼 {job_data.get('title', '')}\n\n"
            f"🏢 {job_data.get('company', '')}\n\n"
            f"📍 {job_data.get('location', ' ')}\n\n"
            f"💻 {job_data.get('site', ' ')}\n\n"
            f"-------------------------\n\n"
        )
        bot.send_message(user_id, search_summary, reply_markup=reply_markup)
        redis_client.lrem(user_id, 1, json.dumps(job_data))
    else:
        bot.send_message(user_id,
        "سعی کردیم جدیدترین آگهی ها رو برات به نمایش بزاریم بزودی امکانی برای کاربرها فراهم میشه که باتوجه به موقعیت شغلی که میخوان اگهی ها براشون ارسال بشه پس تا ائن موقعه کنارمون باش.", )


@bot.callback_query_handler(func=lambda call: call.data.startswith("next:"))
def button_callback(call):
    action, current_index = call.data.split(':')
    current_index = int(current_index)
    send_job(call.message.chat.id, current_index + 1)


bot.infinity_polling()
