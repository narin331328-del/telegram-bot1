import os
import google.generativeai as genai
import telebot
from telebot import types
from dotenv import load_dotenv

# ==========================================
# #CONFIG: ព័ត៌មានសម្ងាត់និងការតភ្ជាប់ API
# ==========================================
load_dotenv()

# ទាញយក Token ពី Railway Variables យ៉ាងถูกต้อง
TELEGRAM_BOT_TOKEN = os.getenv("8812870706:AAE5xxwFgtakXa9DEgxNR_NKG40vgwoqYTg")
GEMINI_API_KEY = os.getenv("tIavwumKg3mWGwOEEXWEmShojYT3svthAXltCH0q")

if not TELEGRAM_BOT_TOKEN:
  raise ValueError("❌ មិនទាន់បានកំណត់ TELEGRAM_BOT_TOKEN ទេ!")

if not GEMINI_API_KEY:
  raise ValueError("❌ មិនទាន់បានកំណត់ GEMINI_API_KEY ទេ!")

# កំណត់ค่า Gemini API
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", generation_config=generation_config
)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# ==========================================
# #HELPER_FUNCTION: បែងចែកអត្ថបទវែងៗ
# ==========================================
def send_long_message(chat_id, text, reply_markup=None):
  max_length = 4000
  if len(text) <= max_length:
    bot.send_message(chat_id, text, reply_markup=reply_markup)
  else:
    parts = [text[i : i + max_length] for i in range(0, len(text), max_length)]
    for idx, part in enumerate(parts):
      if idx == len(parts) - 1:
        bot.send_message(chat_id, part, reply_markup=reply_markup)
      else:
        bot.send_message(chat_id, part)


# ==========================================
# #BOT_COMMANDS
# ==========================================
def set_bot_commands(bot_instance):
  commands = [
      telebot.types.BotCommand("start", "ចាប់ផ្តើមប្រើប្រាស់ Bot"),
      telebot.types.BotCommand("help", "ជំនួយការប្រើប្រាស់"),
  ]
  bot_instance.set_my_commands(commands)


# ==========================================
# #KEYBOARD_UI
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
# #HANDLER_START
# ==========================================
@bot.message_handler(commands=["start"])
def send_welcome(message):
  send_long_message(
      message.chat.id,
      "🌟 សួស្តី! AI Assistant ដ៏ឆ្លាតវៃរបស់អ្នកបានដំណើរការហើយ!\n\n"
      "🤖 ខ្ញុំអាចជួយអ្នកបានគ្រប់យ៉ាង មិនថារឿង Cybersecurity, Coding, "
      "ចំណេះដឹងទូទៅ ឬវិភាគសុវត្ថិភាព Links នោះទេ។\n\n"
      "👇 សូមជ្រើសរើសមុខងារខាងក្រោម ឬសួរសំណួរមកកាន់ខ្ញុំដោយសេរី!",
      reply_markup=get_main_menu(),
  )


# ==========================================
# #HANDLER_HELP
# ==========================================
@bot.message_handler(commands=["help"])
def send_help(message):
  send_long_message(
      message.chat.id,
      "📌 របៀបប្រើប្រាស់ Bot នេះ៖\n"
      "1. Chat Anything: សួរនាំរាល់បញ្ហា IT ឬចំណេះដឹងទូទៅ។\n"
      "2. Security Check: ផ្ញើ Link មកឱ្យ AI វិភាគសុវត្ថិភាព។",
      reply_markup=get_main_menu(),
  )


# ==========================================
# #HANDLER_TEXT_MESSAGES
# ==========================================
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
  try:
    user_input = message.text if message.text else ""

    if user_input == "🛡️ Cybersecurity & IT Pro":
      reply_text = (
          "🛡️ Cybersecurity & Ethical Hacking Hub:\nទីនេះសម្រាប់ពិភាក្សា និងជំនួយការផ្នែក"
          " Pentesting, Network Security, Vulnerability Assessment។"
      )
    elif user_input == "🧠 ចំណេះដឹងទូទៅបច្ចេកវិទ្យា (Tech Knowledge)":
      reply_text = (
          "🧠 ចំណេះដឹងទូទៅផ្នែកបច្ចេកវិទ្យា:\n🌐 អំពី Phishing Links & Cloudflare"
          " Tunnels (`trycloudflare.com`)."
      )
    elif user_input == "🌐 Scan Link / File Security":
      reply_text = (
          "🌐 Security Scanner:\nសូមផ្ញើ URL Link ឬ Code មកកាន់ទីនេះ នោះ AI"
          " នឹងវិភាគរកហានិភ័យជូន។"
      )
    elif user_input == "💻 Programming & Code Debug":
      reply_text = (
          "💻 Programming Assistant:\nផ្ញើកូដ ឬបញ្ហា Programming មក (Python,"
          " JavaScript, etc.) ខ្ញុំនឹងជួយ Debug។"
      )
    elif user_input == "📚 ការសិក្សា និងការអភិវឌ្ឍខ្លួន":
      reply_text = (
          "📚 Study & Self-Development:\nជួយសម្រួលដល់ការសិក្សា និងស្វែងយល់ពីចំណេះដឹងថ្មីៗ។"
      )
    elif user_input == "❓ ជំនួយការប្រើប្រាស់ (Help)":
      reply_text = "📌 របៀបប្រើប្រាស់ Bot នេះ សូមមើលក្នុងเมนูหลัก។"
    else:
      loading_msg = bot.send_message(
          message.chat.id, "⏳ AI កំពុងវិភាគសំណួររបស់អ្នកយ៉ាងម៉ត់ចត់..."
      )

      system_prompt = (
          "You are an elite, world-class AI Assistant with advanced multilingual"
          " intelligence. Communicate in natural, fluent, and warm Khmer"
          " language. Analyze links, code, or queries deeply for security"
          " threats or bugs."
      )

      # ហៅប្រើប្រាស់ Gemini API
      chat = model.start_chat(
          history=[
              {
                  "role": "user",
                  "parts": [
                      f"System Instruction: {system_prompt}\n\nUser Question: {user_input}"
                  ],
              }
          ]
      )
      response = chat.send_message(user_input)
      reply_text = response.text

      try:
        bot.delete_message(message.chat.id, loading_msg.message_id)
      except:
        pass

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


if __name__ == "__main__":
  set_bot_commands(bot)
  try:
    bot.remove_webhook()
  except Exception as e:
    print(f"Remove Webhook Error: {e}")

  print("Bot is running smoothly and ready...")
  bot.infinity_polling(skip_pending=True)
