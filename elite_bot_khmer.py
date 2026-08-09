import os
from google import genai
import telebot

# ដាក់ Token និង API Key របស់អ្នកចូលទៅក្នុងកូដផ្ទាល់
TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
GEMINI_API_KEY = (
    "AQ.Ab8RN6I5zp6Bxr0vvOUh7PT6qiri5q0ekkStluZd97_nMAB6tApast"  # noqa: E501
)

# កំណត់ Client សម្រាប់ Google GenAI SDK ជំនាន់ថ្មី
client = genai.Client(api_key=GEMINI_API_KEY)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "សួស្តី លោក/លោកស្រី! ខ្ញុំជា AI ជំនួយការរបស់អ្នកដែលបំពាក់ដោយ Google"
      " Gemini។ តើថ្ងៃនេះចង់ឱ្យខ្ញុំជួយអ្វីខ្លះ?",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=message.text
    )
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")


if __name__ == "__main__":
  print("Bot is running with Google Gemini...")
  bot.infinity_polling()