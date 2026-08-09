import os
import google.generativeai as genai
import telebot

# ទាញយក Token និង API Key ពី Railway Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6JCFISGzfOQhJfkRO8bZNQ9x-uDUuMKkZjjHXdtw5T1eA")

# កំណត់រចនាសម្ព័ន្ធ Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "សួស្តី លោក/លោកស្រី! ខ្ញុំជា AI ជំនួយការរបស់អ្នកដែលបំពាក់ដោយ Google"
      " Gemini (Free Tier)។ តើថ្ងៃនេះចង់ឱ្យខ្ញុំជួយអ្វីខ្លះ?",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = model.generate_content(message.text)
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")


if __name__ == "__main__":
  print("Bot is running with Google Gemini...")
  bot.infinity_polling()