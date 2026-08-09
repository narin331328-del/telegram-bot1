import os
from google import genai
import telebot

# ទាញយក Token និង API Key ពី Railway Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts")
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6I5zp6Bxr0vvOUh7PT6qiri5q0ekkStluZd97_nMAB6tA")

# ប្រើប្រាស់ SDK ថ្មីសម្រាប់ Key ប្រភេទ AQ...
client = genai.Client(api_key=GEMINI_API_KEY)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "សួស្តី លោក/លោកស្រី! ខ្ញុំជា AI ជំនួយការរបស់អ្នកដែលបំពាក់ដោយ Google"
      " Gemini (New Auth Key)។ តើថ្ងៃនេះចង់ឱ្យខ្ញុំជួយអ្វីខ្លះ?",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    # ប្រើប្រាស់វិធីសាស្ត្រជំនាន់ថ្មីរបស់ Google GenAI SDK
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # ឬ gemini-1.5-flash
        contents=message.text,
    )
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")


if __name__ == "__main__":
  print("Bot is running with Google Gemini (New SDK)...")
  bot.infinity_polling()