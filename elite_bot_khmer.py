import os
import cohere
import telebot

TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
COHERE_API_KEY = "tIavwumKg3mWGwOEEXWEmShojYT3svthAXltCH0q"

try:
  co = cohere.ClientV2(api_key=COHERE_API_KEY)
except Exception as e:
  print(f"Cohere Init Error: {e}")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "សួស្តី! Bot ដំណើរការជោគជ័យហើយ! អ្នកអាចសួរសំណួរ ឬជជែកជាមួយខ្ញុំបាន"
      " គ្រប់សំណួរទាំងអស់!",
  )


@bot.message_handler(commands=["help"])
def send_help(message):
  bot.reply_to(
      message,
      "ជំនួយ៖ អ្នកអាចផ្ញើសារ ឬសួរសំណួរណាមួយមកកាន់ Bot នេះបានភ្លាមៗ។",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = co.chat(
        model="command",  # 👈 ប្រើប្រាស់ model ស្តង់ដារដែលមានស្ថេរភាពល្អបំផុត
        messages=[{"role": "user", "content": message.text}],
    )
    reply_text = response.message.content[0].text
    bot.reply_to(message, reply_text)
  except Exception as e:
    bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")


if __name__ == "__main__":
  bot.infinity_polling()