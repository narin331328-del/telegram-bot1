import os
import cohere
import telebot

TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
# ដាក់ API Key ថ្មី និងត្រឹមត្រូវរបស់អ្នកនៅទីនេះ
COHERE_API_KEY = "EVn3MniDjqKCQvVvE5fDjMxME2KK1oo3ecMdIxR"

try:
  co = cohere.ClientV2(api_key=COHERE_API_KEY)
except Exception as e:
  print(f"Cohere Init Error: {e}")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "សួស្តី! Bot ដំណើរការជោគជ័យហើយ។ អ្នកអាចសួរសំណួរ ឬផ្ញើសារមកកាន់ខ្ញុំបាន!",
  )


@bot.message_handler(commands=["help"])
def send_help(message):
  bot.reply_to(
      message,
      "ជំនួយ៖ អ្នកអាចផ្ញើសារ ឬសំណួរណាមួយមកកាន់ Bot នេះបានភ្លាមៗ"
      " ខ្ញុំនឹងឆ្លើយតបជូនដោយស្វ័យប្រវត្តិ។",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = co.chat(
        model="command",
        messages=[{"role": "user", "content": message.text}],
    )
    reply_text = response.message.content[0].text
    bot.reply_to(message, reply_text)
  except Exception as e:
    bot.reply_to(
        message,
        "សូមអភ័យទោស មានបញ្ហាបន្តិចបន្តួចជាមួយ API Key ឬការតភ្ជាប់ទៅកាន់"
        " AI។ សូមពិនិត្យមើល API Key របស់អ្នកជាថ្មី។",
    )


if __name__ == "__main__":
  bot.infinity_polling()
