import os
import cohere
import telebot
from telebot import types
from dotenv import load_dotenv

# ==========================================
# #CONFIG: ព័ត៌មានសម្ងាត់និងការតភ្ជាប់ API
# ==========================================
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# កំណត់ Timeout ២០វិនាទី ដើម្បីការពារ Error The read operation timed out ពេលផ្ញើ Link ពិនិត្យ
try:
  co = cohere.ClientV2(api_key=COHERE_API_KEY, timeout=20.0)
except Exception as e:
  print(f"Cohere Init Error: {e}")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# ==========================================
# #HELPER_FUNCTION: បែងចែកអត្ថបទវែងៗមិនឱ្យខូចទម្រង់ Telegram
# ==========================================
def send_long_message(chat_id, text, reply_markup=None):
  max_length = 4000
  if len(text) <= max_length:
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
# #BOT_COMMANDS: កំណត់ពាក្យបញ្ជាពេលវាយ /
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
  btn2 = types.KeyboardButton("🧠 ចំណេះដឹងទូទៅបច្ចេកវិទ្យា (Tech Knowledge)")
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
    loading_msg = bot.send_message(
        message.chat.id, "📸 បានទទួលរូបភាពហើយ! AI កំពុងវិភាគ..."
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

    try:
      bot.delete_message(message.chat.id, loading_msg.message_id)
    except:
      pass

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
# #HANDLER_TEXT_MESSAGES: គ្រប់គ្រងការជជែក និងសំណួរអត្ថបទ
# ==========================================
def handle_text_messages(message):
  try:
    user_input = message.text if message.text else ""

    # #EDITABLE_SECTIONS: កន្លែងសម្រាប់កែប្រែអត្ថបទឆ្លើយតបរបស់ប៊ូតុងម៉ឺនុយនីមួយៗ
    if user_input == "🛡️ Cybersecurity & IT Pro":
      reply_text = (
          "🛡️ Cybersecurity & Ethical Hacking Hub:\n"
          "ទីនេះសម្រាប់ពិភាក្សា និងជំនួយការផ្នែក Pentesting, Network Security, "
          "Vulnerability Assessment, និង Device Security (Phone, PC, Laptop)។ "
          "តើអ្នកចង់ឱ្យខ្ញុំជួយពិនិត្យអ្វីថ្ងៃនេះ?"
      )
    elif user_input == "🧠 ចំណេះដឹងទូទៅបច្ចេកវិទ្យា (Tech Knowledge)":
      reply_text = (
          "🧠 ចំណេះដឹងទូទៅផ្នែកបច្ចេកវិទ្យា (Tech General Knowledge):\n\n"
          "🌐 អំពី Phishing Links & Cloudflare Tunnels (`trycloudflare.com`):\n"
          "• តើវាជាអ្វី? វាគឺជាប្រព័ន្ធបង្កើត Tunnel ស្របច្បាប់សម្រាប់ Developers ប៉ុន្តែពួក Hacker "
          "ມັກយកមកបន្លំធ្វើជា Website ក្លែងក្លាយដើម្បីលួច Password ឬ Data របស់អ្នកប្រើប្រាស់។\n"
          "• គន្លឹះការពារ៖ មុននឹងចុចលើ Link អ្វីមួយដែលមានទម្រង់ចម្លែក "
          "សូមផ្ញើ Link นั้นមកកាន់ Bot ນີ້ដើម្បីឱ្យ AI ຊ່ວຍ Scan រកហានិភ័យជាមុនសិន!"
      )
    elif user_input == "🌐 Scan Link / File Security":
      reply_text = (
          "🌐 Security Scanner (Links & Files):\n"
          "សូមផ្ញើ URL Link (ឧទាហរណ៍ Link ຕ່າງៗ) ឬ Code snippet មកកាន់ទីនេះ "
          "នោះ AI នឹងធ្វើការវិភាគយ៉ាងស៊ីជម្រៅថាតើវាមានសុវត្ថិភាព (SAFE) ឬមានគ្រោះថ្នាក់ (DANGEROUS)។"
      )
    elif user_input == "💻 Programming & Code Debug":
      reply_text = (
          "💻 Programming & Scripting Assistant:\n"
          "ផ្ញើកូដ ឬបញ្ហា Programming របស់អ្នកមក (Python, C++, JavaScript, Bash) "
          "ខ្ញុំនឹងជួយរកកំហុស (Debug) និងពន្យល់ពីរបៀបកែសម្រួលយ៉ាងលម្អិត។"
      )
    elif user_input == "📚 ការសិក្សា និងការអភិវឌ្ឍខ្លួន":
      reply_text = (
          "📚 Study & Self-Development:\n"
          "ជួយសម្រួលដល់ការសិក្សា ការធ្វើលំហាត់ ឬស្វែងយល់ពីចំណេះដឹងថ្មីៗ។"
      )
    elif user_input == "❓ ជំនួយការប្រើប្រាស់ (Help)":
      reply_text = (
          "📌 របៀបប្រើប្រាស់ Bot នេះ៖\n"
          "1. Chat Anything: សួរនាំរាល់បញ្ហា IT, Hacking, ឬចំណេះដឹងទូទៅគ្រប់សំណួរ។\n"
          "2. Security Check: ផ្ញើ Link ឬ Text មកដើម្បីឱ្យ AI វិភាគសុវត្ថិភាព។\n"
          "3. Image Analysis: ផ្ញើរូបភាព ឬ Screenshot ឱ្យ AI ຊ່ວຍអាននិងពន្យល់។"
      )
    else:
      # ផ្ញើសារ Loading ជាមុនសិន ដើម្បីការពារកុំឱ្យ Telegram ផ្អាក Timeout ពេល AI គិតយូរ (ពេល Scan Link)
      loading_msg = bot.send_message(
          message.chat.id, "⏳ AI កំពុងវិភាគសំណួរ និងពិនិត្យ Link យ៉ាងម៉ត់ចត់..."
      )

      system_prompt = (
          "You are an elite, world-class AI Assistant (like ChatGPT and Gemini)"
          " with advanced multilingual intelligence. "
          "Communicate in natural, fluent, and warm Khmer language. "
          "When the user sends a Link, URL, Code, or text, analyze it deeply for"
          " security threats, phishing risks, bugs, or factual correctness. "
          "If checking a link safety, explicitly state whether it is SAFE or"
          " DANGEROUS with clear technical reasoning."
      )

      response = co.chat(
          model="command-a-plus-05-2026",
          messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": user_input},
          ],
      )

      try:
        bot.delete_message(message.chat.id, loading_msg.message_id)
      except:
        pass

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
  print("Bot is running smoothly and ready for GitHub deployment...")
  bot.infinity_polling(skip_pending=True)