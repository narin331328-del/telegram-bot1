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


# កំណត់ Command Menu សម្រាប់ Telegram
def set_bot_commands(bot_instance):
  commands = [
      telebot.types.BotCommand(
          "start", "ចាប់ផ្តើមប្រព័ន្ធ AI Cyber Assistant"
      ),
      telebot.types.BotCommand("scan", "វិភាគ Link / File / Code រកសុវត្ថិភាព"),
      telebot.types.BotCommand("code", "ពិនិត្យនិង Debug កូដ Programming"),
      telebot.types.BotCommand("cyber", "ប្រឹក្សាយោបល់ផ្នែក Hacking & Defense"),
      telebot.types.BotCommand("help", "ជំនួយការប្រើប្រាស់"),
  ]
  bot_instance.set_my_commands(commands)


# បង្កើត Menu ប៊ូតុងបញ្ជាអស្ចារ្យនៅខាងក្រោម
def get_main_menu():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn1 = types.KeyboardButton("🛡️ Scan Link / File Security")
  btn2 = types.KeyboardButton("💻 Check & Debug Code")
  btn3 = types.KeyboardButton("🔍 Cyber & Pentest Advisor")
  btn4 = types.KeyboardButton("🖼️ Media & Image Analysis")
  btn5 = types.KeyboardButton("⚡ System Status / Info")
  btn6 = types.KeyboardButton("❓ ជំនួយការប្រើប្រាស់")
  markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
  return markup


# 1. ស្វាគមន៍ /start
@bot.message_handler(commands=["start"])
@bot.message_handler(
    func=lambda msg: msg.text
    and msg.text.strip()
    in ["🏠 ចាប់ផ្តើម", "start", "/start", "ចាប់ផ្តើម"]
)
def send_welcome(message):
  bot.send_message(
      message.chat.id,
      "🛡️ **Elite Cyber AI Assistant បានចាប់ផ្តើមដំណើរការ ១០០%!**\n\n"
      "ខ្ញុំជា AI ជំនួយការផ្ទាល់ខ្លួនរបស់អ្នក (Built for IT & Cybersecurity Students)។"
      " អ្នកអាចឱ្យខ្ញុំជួយ៖\n"
      "🌐 **Scan Links & Files:** ពិនិត្យមើលថាតើមាន Malware, Phishing ឬមានសុវត្ថិភាពដែរឬទេ\n"
      "💻 **Check Code:** ពិនិត្យកូដ កកាយរក Vulnerabilities\n"
      "🖼️ **Media Analysis:** វិភាគរូបភាព វីដេអូ ឬ Screenshots ផ្សេងៗ\n"
      "💬 **Chat Anything 24/7:** សួរនាំរាល់បញ្ហា Networking, Hacking, Programming គ្រប់ Device (Phone, PC, Hardware)\n\n"
      "👇 សូមផ្ញើ Link, File, Code, រូបភាព ឬសួរសំណួរមកកាន់ខ្ញុំបានភ្លាមៗ!",
      reply_markup=get_main_menu(),
      parse_mode="Markdown",
  )


# 2. មុខងារ Scan Link / File / Security
@bot.message_handler(commands=["scan"])
@bot.message_handler(
    func=lambda msg: msg.text and "Scan Link" in msg.text
)
def scan_prompt(message):
  bot.send_message(
      message.chat.id,
      "🔍 **ប្រព័ន្ធ Security Scanner កំពុងរង់ចាំ...**\n\n"
      "សូមផ្ញើ **URL Link**, **ឈ្មោះ File**, ឬ **Code snippet** មកកាន់ទីនេះ"
      " នោះខ្ញុំនឹងធ្វើការវិភាគយ៉ាងក្បោះក្បាយ (Risk Assessment, Threat Analysis"
      " & Safety Status) ជូនអ្នកភ្លាមៗ!",
      reply_markup=get_main_menu(),
  )


# 3. មុខងារ Check & Debug Code
@bot.message_handler(commands=["code"])
@bot.message_handler(
    func=lambda msg: msg.text and "Check & Debug" in msg.text
)
def code_prompt(message):
  bot.send_message(
      message.chat.id,
      "💻 **Code Security & Debugging Hub:**\nផ្ញើកូដរបស់អ្នកមកទីនេះ (Python, C++,"
      " Bash, JS, PowerShell, v.v.) ខ្ញុំនឹងជួយរកកំហុស (Bugs), ពិនិត្យរឿង"
      " Vulnerabilities (Security Flaws) និងសរសរបន្ថែមឱ្យបានកាន់តែប្រសើរ។",
      reply_markup=get_main_menu(),
  )


# 4. មុខងារ Cyber & Pentest
@bot.message_handler(commands=["cyber"])
@bot.message_handler(
    func=lambda msg: msg.text and "Cyber & Pentest" in msg.text
)
def cyber_prompt(message):
  bot.send_message(
      message.chat.id,
      "🛡️ **Ethical Hacking & Defense Advisor:**\nសួរសំណួរពាក់ព័ន្ធនឹង Pentesting,"
      " Exploit development, Network sniffing, Cisco routing, ឬ System"
      " hardening លើ Phone/PC/Hardware បានគ្រប់ពេល។",
      reply_markup=get_main_menu(),
  )


# 5. មុខងារ Help
@bot.message_handler(commands=["help"])
@bot.message_handler(
    func=lambda msg: msg.text and "ជំនួយការប្រើប្រាស់" in msg.text
)
def send_help(message):
  bot.send_message(
      message.chat.id,
      "📌 **របៀបប្រើប្រាស់ AI Assistant ផ្ទាល់ខ្លួន៖**\n1. **ផ្ញើ Link/File/Text:**"
      " ដើម្បីឱ្យ AI វិភាគសុវត្ថិភាព។\n2. **ផ្ញើរូបភាព ឬ Screenshot:** AI"
      " នឹងអាននិងពន្យល់ពីកំហុសក្នុងរូបភាពនោះ។\n3. **សួរនាំរាល់បញ្ហា IT:** មិនថាជា"
      " Coding, Networking ឬ Hacking ទេ។",
      reply_markup=get_main_menu(),
  )


# 6. ទទួលការផ្ញើរូបភាព (Photos / Screenshots) មកវិភាគ
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
  try:
    # យក File ID របស់រូបភាពដែល User ផ្ញើមក
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    file_path = file_info.file_path

    # ផ្ញើសារដំណឹងជូន User វិញ
    bot.reply_to(
        message,
        "📸 បានទទួលរូបភាពរបស់អ្នកហើយ! AI កំពុងវិភាគរូបភាព និងស្វែងរកព័ត៌មានលម្អិត..."
    )

    # ឱ្យ AI ឆ្លើយតបវិភាគរូបភាព (ឆ្លើយជាភាសាខ្មែរ)
    response = co.chat(
        model="command-a-plus-05-2026",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an elite Cybersecurity Expert and IT Assistant."
                    " The user sent an image/screenshot. Analyze it professionally"
                    " (e.g., if it's code, error logs, network topology, or"
                    " interface) and explain everything in clear, natural"
                    " Khmer language with technical accuracy."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Please analyze this image sent by the user and provide a"
                    " technical breakdown."
                ),
            },
        ],
    )

    reply_text = response.message.content[0].text
    bot.send_message(
        message.chat.id,
        f"🔍 **លទ្ធផលវិភាគរូបភាព៖**\n\n{reply_text}",
        reply_markup=get_main_menu(),
    )
  except Exception as e:
    bot.send_message(
        message.chat.id,
        f"⚠️ កំហុសក្នុងការអានរូបភាព៖ {str(e)}",
        reply_markup=get_main_menu(),
    )


# 7. ទទួលរាល់សារ ឯកសារ Links និងការសន្ទនាទូទៅ (Chat Anything & Security Link/File Check)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    user_input = message.text

    # ប្រសិនបើ User ផ្ញើ Link ឬ Code ឬសំណួរមក ឱ្យ AI វិភាគសុវត្ថិភាពនិងការពិតក្បោះក្បាយ
    system_prompt = (
        "You are an elite, world-class AI Cybersecurity Expert, Ethical Hacker,"
        " Network Engineer, and Senior Programmer acting as the user's"
        " personal assistant. "
        "When the user sends a Link, URL, Code, or text, analyze it deeply for"
        " security threats, vulnerabilities, phishing risks, or bugs. "
        "Always give truthful, detailed, step-by-step, and professional"
        " answers. "
        "If checking a link or file safety, explicitly state whether it is SAFE"
        " or DANGEROUS, giving clear reasons. "
        "Always reply in clear, professional, and natural Khmer language,"
        " blending precise technical terms."
    )

    response = co.chat(
        model="command-a-plus-05-2026",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
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
        reply_text
        if reply_text
        else "⚠️ សូមអភ័យទោស ប្រព័ន្ធមិនទាន់ទទួលបានទិន្នន័យឆ្លើយតប។",
        reply_markup=get_main_menu(),
    )
  except Exception as e:
    bot.send_message(
        message.chat.id,
        f"⚠️ កំហុសបច្ចេកទេស (Error): {str(e)}",
        reply_markup=get_main_menu(),
    )


if __name__ == "__main__":
  set_bot_commands(bot)
  bot.infinity_polling()