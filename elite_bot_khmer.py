import os
import cohere
import telebot
from telebot import types

TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
COHERE_API_KEY = "tIavwumKg3mWGwOEEXWEmShojYT3svthAXltCH0q"

try:
  co = cohere.ClientV2(api_key=COHERE_API_KEY)
except Exception as e:
  print(f"Cohere Init Error: {e}")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# បង្កើត Menu ប៊ូតុងនៅខាងក្រោមប្រអប់សារ
def get_main_menu():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn1 = types.KeyboardButton("🏠 ចាប់ផ្តើម (Start)")
  btn2 = types.KeyboardButton("❓ ជំនួយ (Help)")
  btn3 = types.KeyboardButton("⚙️ មុខងារផ្សេងៗ (Menu)")
  btn4 = types.KeyboardButton("✨ អំពីខ្ញុំ (About)")
  markup.add(btn1, btn2, btn3, btn4)
  return markup


# ទទួលពាក្យ "start" ឬ "/start" ដោយមិនបាច់ប្រើ /
@bot.message_handler(
    func=lambda message: message.text
    and message.text.lower().strip() in ["start", "/start", "ចាប់ផ្តើម"]
)
def send_welcome(message):
  bot.send_message(
      message.chat.id,
      "សួស្តី! Bot ដំណើរការជោគជ័យហើយ! អ្នកអាចសួរសំណួរ ឬជជែកជាភាសាខ្មែរជាមួយខ្ញុំបាន"
      " គ្រប់សំណួរទាំងអស់។",
      reply_markup=get_main_menu(),
  )


# ទទួលពាក្យ "help" ឬ "/help"
@bot.message_handler(
    func=lambda message: message.text
    and message.text.lower().strip() in ["help", "/help", "ជំនួយ"]
)
def send_help(message):
  bot.send_message(
      message.chat.id,
      "ជំនួយ៖ អ្នកអាចផ្ញើសារ ឬសួរសំណួរណាមួយមកកាន់ Bot នេះបានភ្លាមៗ។",
      reply_markup=get_main_menu(),
  )


# មុខងារ Coming Soon សម្រាប់ប៊ូតុងផ្សេងៗ
@bot.message_handler(
    func=lambda message: message.text
    and message.text.strip() in ["⚙️ មុខងារផ្សេងៗ (Menu)", "✨ អំពីខ្ញុំ (About)"]
)
def coming_soon(message):
  bot.send_message(
      message.chat.id,
      "⚠️ ទិន្នន័យនឹងមិនទាន់បានដាក់អោយប្រើការទេ it’s coming soon!",
      reply_markup=get_main_menu(),
  )


# ឆ្លើយតបគ្រប់សំណួរជជែកលេងទាំងអស់ជាភាសាខ្មែរ
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
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

    bot.send_message(
        message.chat.id,
        reply_text if reply_text else "សូមអភ័យទោស ខ្ញុំមិនបានទទួលអត្ថបទទេ។",
        reply_markup=get_main_menu(),
    )
  except Exception as e:
    bot.send_message(
        message.chat.id,
        f"មានបញ្ហាបន្តិច៖ {str(e)}",
        reply_markup=get_main_menu(),
    )


if __name__ == "__main__":
  bot.infinity_polling()
