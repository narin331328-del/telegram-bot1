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


# កំណត់ម៉ឺនុយពាក្យបញ្ជា (Commands Menu) ឱ្យលោតចេញជាภาษาខ្មែរពេលវាយសញ្ញា /
def set_bot_commands(bot_instance):
  commands = [
      telebot.types.BotCommand("start", "ចាប់ផ្តើមប្រើប្រាស់ Bot"),
      telebot.types.BotCommand("help", "ជំនួយនិងរបៀបប្រើប្រាស់"),
      telebot.types.BotCommand("daily", "សំណួរប្រចាំថ្ងៃសម្រាប់សួររាល់ថ្ងៃ"),
      telebot.types.BotCommand("about", "ព័ត៌មានលម្អិតអំពី Bot នេះ"),
  ]
  bot_instance.set_my_commands(commands)


# 1. បង្កើត Menu ប៊ូតុងនៅខាងក្រោមប្រអប់សារ
def get_main_menu():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn1 = types.KeyboardButton("🏠 ចាប់ផ្តើម")
  btn2 = types.KeyboardButton("❓ ជំនួយ")
  btn3 = types.KeyboardButton("💡 សំណួរប្រចាំថ្ងៃ")
  btn4 = types.KeyboardButton("✨ អំពីខ្ញុំ")
  markup.add(btn1, btn2, btn3, btn4)
  return markup


# ពាក្យបញ្ជា /start និងប៊ូតុង
@bot.message_handler(
    commands=["start"],
    func=lambda msg: msg.text
    and msg.text.strip() in ["🏠 ចាប់ផ្តើម", "start", "ចាប់ផ្តើម"],
)
def send_welcome(message):
  bot.send_message(
      message.chat.id,
      "សួស្តី! 🤖 Bot របស់អ្នកត្រូវបានរៀបចំយ៉ាងពិសេសរួចរាល់ហើយ! អ្នកអាចសួរសំណួរ"
      " ឬជជែកជាភាសាខ្មែរជាមួយខ្ញុំបានគ្រប់សំណួរទាំងអស់។",
      reply_markup=get_main_menu(),
  )


# ពាក្យបញ្ជា /help
@bot.message_handler(
    commands=["help"],
    func=lambda msg: msg.text
    and msg.text.strip() in ["❓ ជំនួយ", "help", "ជំនួយ"],
)
def send_help(message):
  bot.send_message(
      message.chat.id,
      "📌 **របៀបប្រើប្រាស់៖**\n- អ្នកអាចជជែកសួរនាំអ្វីក៏បានជាមួយ AI ផ្ទាល់។\n-"
      " អាចចុចលើប៊ូតុងខាងក្រោមដើម្បីជ្រើសរើសមុខងារផ្សេងៗ។",
      reply_markup=get_main_menu(),
      parse_mode="Markdown",
  )


# ពាក្យបញ្ជា /about
@bot.message_handler(
    commands=["about"],
    func=lambda msg: msg.text and msg.text.strip() in ["✨ អំពីខ្ញុំ", "about"],
)
def about_bot(message):
  bot.send_message(
      message.chat.id,
      "🤖 ខ្ញុំគឺជាជំនួយការ AI ដ៏ឆ្លាតវៃ បង្កើតឡើងដើម្បីជួយសម្រួលការងារ និងការសន្ទនារបស់អ្នកជាភាសាខ្មែរយ៉ាងរលូន!",
      reply_markup=get_main_menu(),
  )


# ពាក្យបញ្ជា /daily (សំណួរប្រចាំថ្ងៃ)
@bot.message_handler(
    commands=["daily"],
    func=lambda msg: msg.text and msg.text.strip() == "💡 សំណួរប្រចាំថ្ងៃ",
)
def daily_questions(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
  markup.add(
      types.KeyboardButton("🌟 ផ្តល់យោបល់លើការលើកទឹកចិត្តថ្ងៃនេះ"),
      types.KeyboardButton("💻 គន្លឹះរៀនសរសេរកូដកុំព្យូទ័រ"),
      types.KeyboardButton("🥗 យោបល់ហាត់ប្រាណនិងសុខភាព"),
      types.KeyboardButton("🔙 ត្រឡប់ក្រោយ"),
  )
  bot.send_message(
      message.chat.id,
      "💡 សូមជ្រើសរើសប្រធានបទសំណួរប្រចាំថ្ងៃដែលអ្នកចង់សួរ៖",
      reply_markup=markup,
  )


# ប៊ូតុងត្រឡប់ក្រោយ
@bot.message_handler(
    func=lambda msg: msg.text and msg.text.strip() == "🔙 ត្រឡប់ក្រោយ"
)
def go_back(message):
  bot.send_message(
      message.chat.id, "🔙 បានត្រឡប់មកម៉ឺនុយដើមវិញ។", reply_markup=get_main_menu()
  )


# ឆ្លើយតបគ្រប់សំណួរជជែកលេងទូទៅ (Chat Anything) ជាភាសាខ្មែរ
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = co.chat(
        model="command-a-plus-05-2026",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an advanced, friendly AI assistant. Always reply"
                    " in clear, natural, and polite Khmer language."
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
  set_bot_commands(bot)  # កំណត់ Menu Command ពេលចាប់ផ្តើមរត់ Bot
  bot.infinity_polling()
