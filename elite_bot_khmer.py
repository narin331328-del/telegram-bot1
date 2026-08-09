import os
import cohere
import telebot
from telebot import types

# ==========================================
# #CONFIG: ព័ត៌មានសម្ងាត់និងការតភ្ជាប់ API
# ==========================================
TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
COHERE_API_KEY = "tIavwumKg3mWGwOEEXWEmShojYT3svthAXltCH0q"

try:
  co = cohere.ClientV2(api_key=COHERE_API_KEY)
except Exception as e:
  print(f"Cohere Init Error: {e}")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# ==========================================
# #HELPER_FUNCTION: បែងចែកអត្ថបទវែង និងការពារ Error Markdown
# ==========================================
def send_long_message(chat_id, text, reply_markup=None):
  max_length = 4000
  if len(text) <= max_length:
    # #NOTE: ដក parse_mode ចេញ ដើម្បីការពារកុំឱ្យខូចទម្រង់ Markdown របស់ Telegram
    bot.send_message(chat_id, text, reply_markup=reply_markup)
  else:
    parts = [
        text[i : i + max_length] for i in range(0, len(text), max_length)
    ]
    for idx, part in enumerate(parts):
      if idx == len(parts) - 1:
        bot.send_message(chat_id, part, reply_markup=reply_markup)
      else:
        bot.send_message(chat_id, part)


# ==========================================
# #MENU_COMMANDS: បញ្ជីពាក្យបញ្ជាពេលវាយសញ្ញា /
# ==========================================
def set_bot_commands(bot_instance):
  commands = [
      telebot.types.BotCommand("start", "ចាប់ផ្តើមប្រើប្រាស់ Bot"),
      telebot.types.BotCommand("help", "ជំនួយការប្រើប្រាស់"),
  ]
  bot_instance.set_my_commands(commands)


# ==========================================
# #KEYBOARD_UI: ប៊ូតុងម៉ឺនុយនៅខាងក្រោមប្រអប់សារ
# ==========================================
def get_main_menu():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn1 = types.KeyboardButton("🛡️ Cybersecurity & IT Pro")
  btn2 = types.KeyboardButton("🧠 ចំណេះដឹងទូទៅ (General Knowledge)")
  btn3 = types.KeyboardButton("🌐 Scan Link / File Security")
  btn4 = types.KeyboardButton("💻 Programming & Code Debug")
  btn5 = types.KeyboardButton("📚 ការសិក្សា និងការអភិវឌ្ឍខ្លួន")
  btn6 = types.KeyboardButton("❓ ជំនួយការប្រើប្រាស់ (Help)")
  markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
  return markup


# ==========================================
# #HANDLER_START: ការចាប់ផ្តើម /start
# ==========================================
@bot.message_handler(commands=["start"])
def send_welcome(message):
  send_long_message(
      message.chat.id,
      "🌟 សួស្តី! AI Assistant ដ៏ឆ្លាតវៃរបស់អ្នកបានដំណើរការហើយ!\n\n"
      "🤖 ខ្ញុំអាចជួយអ្នកបានគ្រប់យ៉ាង មិនថារឿង Cybersecurity, Coding, ចំណេះដឹងទូទៅ "
      "ឬវិភាគសុវត្ថិភាព Links/Files នោះទេ។ អាចជជែកសួរនាំខ្ញុំបានដូច ChatGPT និង Gemini ដែរ!\n\n"
      "👇 សូមជ្រើសរើសមុខងារខាងក្រោម ឬសួរសំណួរមកកាន់ខ្ញុំដោយសេរី!",
      reply_markup=get_main_menu(),
  )


# ==========================================
# #HANDLER_HELP: ជំនួយការប្រើប្រាស់ (/help)
# ==========================================
@bot.message_handler(commands=["help"])
def send_help(message):
  send_long_message(
      message.chat.id,
      "📌 របៀបប្រើប្រាស់ Bot នេះ៖\n"
      "1. Chat Anything: សួរនាំរាល់បញ្ហា IT, Hacking, ឬចំណេះដឹងទូទៅគ្រប់សំណួរ។\n"
      "2. Security Check: ផ្ញើ Link ឬ Text មកដើម្បីឱ្យ AI វិភាគសុវត្ថិភាព។\n"
      "3. Image Analysis: ផ្ញើរូបភាព ឬ Screenshot ឱ្យ AI ຊ່ວຍអាននិងពន្យល់។",
      reply_markup=get_main_menu(),
  )


# ==========================================
# #HANDLER_PHOTOS: ទទួល និងវិភាគរូបភាព ឬ Screenshots
# ==========================================
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
  try:
    bot.reply_to(
        message, "📸 បានទទួលរូបភាពហើយ! AI កំពុងវិភាគយ៉ាងយកចិត្តទុកដាក់..."
    )

    response = co.chat(
        model="command-a-plus-05-2026",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an elite AI Assistant. The user sent an image."
                    " Analyze it thoroughly and explain everything clearly in"
                    " natural Khmer language."
                ),
            },
            {
                "role": "user",
                "content": "Please analyze this image and explain what it is.",
            },
        ],
    )

    reply_text = ""
    if hasattr(response, "message") and hasattr(response.message, "content"):
      reply_content = response.message.content
      if isinstance(reply_content, list):
        for item in reply_content:
          if hasattr(item, "text"):
            reply_text += item.text
      else:
        reply_text = str(reply_content)

    send_long_message(
        message.chat.id,
        f"🔍 លទ្ធផលវិភាគរូបភាព៖\n\n{reply_text}"
        if reply_text
        else "⚠️ រូបភាពត្រូវបានវិភាគ ប៉ុន្តែគ្មានអត្ថបទត្រឡប់មកវិញទេ។",
        reply_markup=get_main_menu(),
    )
  except Exception as e:
    send_long_message(
        message.chat.id,
        f"⚠️ កំហុសក្នុងការអានរូបភាព៖ {str(e)}",
        reply_markup=get_main_menu(),
    )


# ==========================================
# #HANDLER_TEXT_MESSAGES: គ្រប់គ្រងសារអត្ថបទទាំងអស់
# ==========================================
def handle_text_messages(message):
  try:
    user_input = message.text if message.text else ""

    if user_input == "🛡️ Cybersecurity & IT Pro":
      reply_text = (
          "🛡️ Cybersecurity & Ethical Hacking Hub:\n"
          "ទីនេះសម្រាប់ពិភាក្សា និងជំនួយការផ្នែក Pentesting, Network Security, "
          "Vulnerability Assessment, និង Device Security (Phone, PC, Laptop, Hardware)។ "
          "តើអ្នកចង់ឱ្យខ្ញុំជួយវិភាគអ្វីថ្ងៃនេះ?"
      )
    elif user_input == "🧠 ចំណេះដឹងទូទៅ (General Knowledge)":
      reply_text = (
          "🧠 General Knowledge & Daily Assistant:\n"
          "ទីនេះសម្រាប់សួរសំណួរទូទៅ វិទ្យាសាស្ត្រ ប្រវត្តិសាស្ត្រ សុខភាព គន្លឹះជីវិត "
          "និងការសិក្សាប្រចាំថ្ងៃ។ តើអ្នកចង់ស្វែងយល់ពីអ្វី?"
      )
    elif user_input == "🌐 Scan Link / File Security":
      reply_text = (
          "🌐 Security Scanner (Links & Files):\n"
          "សូមផ្ញើ URL Link, ឈ្មោះ File, ឬ Code snippet មកកាន់ទីនេះ "
          "នោះខ្ញុំនឹងធ្វើការវិភាគយ៉ាងក្បោះក្បាយ ថាតើវាមានសុវត្ថិភាព (Safe) ឬមានគ្រោះថ្នាក់។"
      )
    elif user_input == "💻 Programming & Code Debug":
      reply_text = (
          "💻 Programming & Scripting Assistant:\n"
          "ផ្ញើកូដ ឬបញ្ហា Programming របស់អ្នកមក (Python, C++, JavaScript, Bash, v.v.) "
          "ខ្ញុំនឹងជួយរកកំហុស (Debug) និងពន្យល់ពីរបៀបកែសម្រួលយ៉ាងលម្អិត។"
      )
    elif user_input == "📚 ការសិក្សា និងការអភិវឌ្ឍខ្លួន":
      reply_text = (
          "📚 Study & Self-Development:\n"
          "ជួយសម្រួលដល់ការសិក្សា ការធ្វើលំហាត់ សរសេរបាយការណ៍ ឬបង្កើតគម្រោងផែនការផ្សេងៗ។"
      )
    elif user_input == "❓ ជំនួយការប្រើប្រាស់ (Help)":
      reply_text = (
          "📌 របៀបប្រើប្រាស់ Bot នេះ៖\n"
          "1. Chat Anything: សួរនាំរាល់បញ្ហា IT, Hacking, ឬចំណេះដឹងទូទៅគ្រប់សំណួរ។\n"
          "2. Security Check: ផ្ញើ Link ឬ Text មកដើម្បីឱ្យ AI វិភាគសុវត្ថិភាព។\n"
          "3. Image Analysis: ផ្ញើរូបភាព ឬ Screenshot ឱ្យ AI ຊ່ວຍអាននិងពន្យល់។"
      )
    else:
      system_prompt = (
          "You are an elite, world-class AI Assistant (like ChatGPT and Gemini)"
          " designed to answer anything accurately and chat about everything. "
          "You have deep expertise in Cybersecurity, Ethical Hacking, Networking,"
          " Programming, Device Security, and General Knowledge for all ages. "
          "When the user sends a Link, URL, Code, or text, analyze it deeply for"
          " security threats, phishing risks, bugs, or factual correctness. "
          "If checking a link or file safety, explicitly state whether it is SAFE"
          " or DANGEROUS with clear reasons. "
          "Always reply in clear, professional, warm, and natural Khmer language,"
          " blending precise technical terms when necessary. Do NOT use broken"
          " markdown symbols that break telegram formatting."
      )

      response = co.chat(
          model="command-a-plus-05-2026",
          messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": user_input},
          ],
      )

      reply_text = ""
      if hasattr(response, "message") and hasattr(response.message, "content"):
        reply_content = response.message.content
        if isinstance(reply_content, list):
          for item in reply_content:
            if hasattr(item, "text"):
              reply_text += item.text
        else:
          reply_text = str(reply_content)

    send_long_message(
        message.chat.id,
        reply_text
        if reply_text
        else "⚠️ សូមអភ័យទោស ប្រព័ន្ធមិនទាន់ទទួលបានទិន្នន័យឆ្លើយតប។",
        reply_markup=get_main_menu(),
    )
  except Exception as e:
    send_long_message(
        message.chat.id,
        f"⚠️ កំហុសបច្ចេកទេស (Error): {str(e)}",
        reply_markup=get_main_menu(),
    )


bot.register_message_handler(handle_text_messages, content_types=["text"])


if __name__ == "__main__":
  set_bot_commands(bot)
  print("Bot is running stably without Markdown parse errors...")
  bot.infinity_polling(skip_pending=True)