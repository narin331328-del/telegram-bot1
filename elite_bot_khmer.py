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
      "សួស្តី! Bot ដំណើរការជោគជ័យហើយ! អ្នកអាចសួរសំណួរ ឬជជែកជាភាសាខ្មែរជាមួយខ្ញុំបាន"
      " គ្រប់សំណួរទាំងអស់។",
  )


@bot.message_handler(commands=["help"])
def send_help(message):
  bot.reply_to(
      message,
      "ជំនួយ៖ អ្នកអាចផ្ញើសារ ឬសួរសំណួរណាមួយមកកាន់ Bot នេះបានភ្លាមៗ។",
  )


@bot.message_handler(commands=["menu", "settings", "profile", "scan"])
def coming_soon(message):
  bot.reply_to(
      message,
      "⚠️ ទិន្នន័យនឹងមិនទាន់បានដាក់អោយប្រើការទេ it’s coming soon!",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    # បន្ថែម System Prompt ដើម្បីបង្គាប់ឱ្យ AI ឆ្លើយជាភាសាខ្មែរជានិច្ច
    response = co.chat(
        model="command-a-plus-05-2026",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Always reply in clear and"
                    " natural Khmer language."
                ),
            },
            {"role": "user", "content": message.text},
        ],
    )

    # កែតម្រូវការទាញយក text ពី response ម៉ូឌែលថ្មី ដើម្បីកុំឱ្យលោត Error object has no attribute text
    reply_content = response.message.content
    if isinstance(reply_content, list):
      reply_text = "".join(
          [
              item.text
              if hasattr(item, "text")
              else getattr(item, "get", lambda x: "")("text", str(item))
              for item in reply_content
          ]
      )
    else:
      reply_text = str(reply_content)

    bot.reply_to(
        message, reply_text if reply_text else "សូមអភ័យទោស ខ្ញុំមិនបានទទួលអត្ថបទទេ។"
    )
  except Exception as e:
    bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")


if __name__ == "__main__":
  bot.infinity_polling()
