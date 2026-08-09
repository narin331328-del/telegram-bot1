import os
import cohere
import telebot

TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
COHERE_API_KEY = "EVn3MniDjqKCQvVvE5fDjMxME2KK1oo3ecMdIxR"

co = cohere.ClientV2(api_key=COHERE_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "សួស្តី! Bot ដំណើរការហើយជាមួយ Cohere AI។")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = co.chat(
        model="command-a",  # 👈 ដូរមកប្រើ model នេះវិញទើបមិន Error 404
        messages=[{"role": "user", "content": message.text}],
    )
    reply_text = response.message.content[0].text
    bot.reply_to(message, reply_text)
  except Exception as e:
    bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")


if __name__ == "__main__":
  bot.infinity_polling()
