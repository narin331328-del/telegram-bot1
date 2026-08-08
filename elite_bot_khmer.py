import os
import telebot
from telebot import types
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google import generativeai as genai

# យក Key ប្រភេទ AQ... របស់អ្នកមកដាក់ទីនេះ
ACCESS_TOKEN = "AQ.Ab8RN6Jy-LdyGdnf_pPRYIfAMtM859ca0Cz..." 

TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"

# កំណត់សិទ្ធិប្រើប្រាស់ OAuth Token ជាមួយ Gemini
credentials = Credentials(token=ACCESS_TOKEN)
genai.configure(credentials=credentials)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("💡 ជំនួយ (Help)")
    item2 = types.KeyboardButton("🤖 អំពីខ្ញុំ (About)")
    markup.add(item1, item2)
    bot.reply_to(message, "សួស្តី! ខ្ញុំជា AI Bot របស់អ្នក។ តើខ្ញុំអាចជួយអ្វីអ្នកថ្ងៃនេះ?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    try:
        if text == "💡 ជំនួយ (Help)":
            bot.reply_to(message, "អ្នកអាចសាកសួររាល់សំណួរ ឬបញ្ជាផ្សេងៗទៅកាន់ខ្ញុំបានដោយសេរី!")
        elif text == "🤖 អំពីខ្ញុំ (About)":
            bot.reply_to(message, "ខ្ញុំជា Telegram Bot ដែលขับเคลื่อนដោយ Google Gemini AI!")
        else:
            response = model.generate_content(text)
            bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")

if __name__ == "__main__":
    print("Bot is running successfully with OAuth token...")
    bot.infinity_polling()