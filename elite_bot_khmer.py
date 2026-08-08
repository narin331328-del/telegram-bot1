import os
import telebot
from google import generativeai as genai

TELEGRAM_BOT_TOKEN = os.environ.get("8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts")
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6JN-EEX1iyIyWjQtLbATGHBhDSQ0BWs5F39mOASDghSjA")

genai.configure(api_key=AQ.Ab8RN6JN-EEX1iyIyWjQtLbATGHBhDSQ0BWs5F39mOASDghSjA)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

bot = telebot.TeleBot(8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_message = message.text
        response = model.generate_content(user_message)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")

if __name__ == "__main__":
    print("Bot is starting and running...")
    bot.infinity_polling()
