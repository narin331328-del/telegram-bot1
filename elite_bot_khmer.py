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
      telebot.types.BotCommand("start", "ចាប់ផ្តើមប្រើប្រាស់ Bot ទាំងអស់គ្នា"),
      telebot.types.BotCommand("cyber", "មុខងារ Cybersecurity & IT ប្រកបដោយវិជ្ជាជីវៈ"),
      telebot.types.BotCommand("general", "ចំណេះដឹងទូទៅ និងជំនួយការរស់នៅប្រចាំថ្ងៃ"),
      telebot.types.BotCommand("scan", "ពិនិត្យសុវត្ថិភាព Link / File / Code"),
      telebot.types.BotCommand("help", "ជំនួយការប្រើប្រាស់"),
  ]
  bot_instance.set_my_commands(commands)


# បង្កើត Menu ប៊ូតុងបញ្ជាទូលំទូលាយសម្រាប់គ្រប់វ័យ និងគ្រប់វិស័យ
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
      "🌟 **សួស្តី! AI Assistant ដ៏ឆ្លាតវៃបានចាប់ផ្តើមដំណើរការហើយ!**\n\n"
      "🤖 Bot នេះត្រូវបានរចនាឡើងយ៉ាងពិសេស ដើម្បីបំពេញតម្រូវការ **គ្រប់មនុស្សគ្រប់វ័យ**៖\n"
      "🔹 **សម្រាប់អ្នកជំនាញ IT & Cybersecurity:** វិភាគ Hacking, Networking, Code, និង Hardware Security។\n"
      "🔹 **សម្រាប់សាធារណជនទូទៅ:** ចំណេះដឹងទូទៅ វិទ្យាសាស្ត្រ ប្រវត្តិសាស្ត្រ សុខភាព គន្លឹះជីវិត និងជំនួយការសិក្សា។\n"
      "🔹 **Security Scan:** ពិនិត្យសុវត្ថិភាពតំណភ្ជាប់ (Links) និងឯកសារថាតើមានសុវត្ថិភាពដែរឬទេ។\n\n"
      "👇 សូមជ្រើសរើសមុខងារខាងក្រោម ឬសួរសំណួរមកកាន់ខ្ញុំដោយសេរី!",
      reply_markup=get_main_menu(),
      parse_mode="Markdown",
  )


# 2. មុខងារ Cybersecurity & IT Pro
@bot.message_handler(commands=["cyber"])
@bot.message_handler(
    func=lambda msg: msg.text and "Cybersecurity & IT Pro" in msg.text
)
def cyber_prompt(message):
  bot.send_message(
      message.chat.id,
      "🛡️ **Cybersecurity & Ethical Hacking Hub:**\n"
      "ទីនេះគឺជាកន្លែងសម្រាប់ពិភាក្សា និងជំនួយការផ្នែក Pentesting, Network Security, "
      "Vulnerability Assessment, និង Hardware Hacking លើ Device ទាំងអស់ (Phone, PC, Laptop)។ "
      "តើអ្នកចង់ឱ្យខ្ញុំជួយវិភាគអ្វីថ្ងៃនេះ?",
      reply_markup=get_main_menu(),
  )


# 3. មុខងារ ចំណេះដឹងទូទៅ (General Knowledge)
@bot.message_handler(commands=["general"])
@bot.message_handler(
    func=lambda msg: msg.text and "ចំណេះដឹងទូទៅ" in msg.text
)
def general_knowledge_prompt(message):
  bot.send_message(
      message.chat.id,
      "🧠 **General Knowledge & Daily Assistant:**\n"
      "ទីនេះសម្រាប់មនុស្សគ្រប់វ័យ! អ្នកអាចសួរនាំអំពីរឿងរ៉ាវទូទៅ វិទ្យាសាស្ត្រ ភូមិសាស្ត្រ ប្រវត្តិសាស្ត្រ "
      "គន្លឹះថែទាំសុខភាព ការធ្វើអាជីវកម្ម ការសិក្សា និងចម្ងល់ផ្សេងៗក្នុងជីវិតប្រចាំថ្ងៃ។ "
      "តើអ្នកចង់ស្វែងយល់ពីអ្វី?",
      reply_markup=get_main_menu(),
  )


# 4. មុខងារ Scan Link / File
@bot.message_handler(commands=["scan"])
@bot.message_handler(
    func=lambda msg: msg.text and "Scan Link" in msg.text
)
def scan_prompt(message):
  bot.send_message(
      message.chat.id,
      "🌐 **Security Scanner (Links & Files):**\n"
      "សូមផ្ញើ **URL Link**, **ឈ្មោះ File**, ឬ **Code snippet** មកកាន់ទីនេះ នោះខ្ញុំនឹងធ្វើការវិភាគយ៉ាងក្បោះក្បាយ "
      "ថាតើវាមានសុវត្ថិភាព (Safe) ឬមានគ្រោះថ្នាក់ (Phishing/Malware) មុនពេលអ្នកចុចចូលមើល!",
      reply_markup=get_main_menu(),
  )


# 5. មុខងារ Programming & Code Debug
@bot.message_handler(
    func=lambda msg: msg.text and "Programming & Code Debug" in msg.text
)
def code_prompt(message):
  bot.send_message(
      message.chat.id,
      "💻 **Programming & Scripting Assistant:**\n"
      "ផ្ញើកូដ ឬបញ្ហា Programming របស់អ្នកមក (Python, C++, JavaScript, Bash, v.v.) "
      "ខ្ញុំនឹងជួយរកកំហុស (Debug) និងពន្យល់ពីរបៀបแก้កែសម្រួលយ៉ាងលម្អិត។",
      reply_markup=get_main_menu(),
  )


# 6. មុខងារ ការសិក្សា និងការអភិវឌ្ឍខ្លួន
@bot.message_handler(
    func=lambda msg: msg.text and "ការសិក្សា និងការអភិវឌ្ឍខ្លួន" in msg.text
)
def study_prompt(message):
  bot.send_message(
      message.chat.id,
      "📚 **Study & Self-Development:**\n"
      "ជួយសម្រួលដល់ការសិក្សារបស់សិស្ស និស្សិត និងអ្នកចង់អភិវឌ្ឍខ្លួន។ "
      "អាចសុំឱ្យខ្ញុំពន្យល់មេរៀន ធ្វើលំហាត់ សរសេរបាយការណ៍ ឬបង្កើតគម្រោងផែនការសិក្សាបាន។",
      reply_markup=get_main_menu(),
  )


# 7. មុខងារ Help
@bot.message_handler(commands=["help"])
@bot.message_handler(
    func=lambda msg: msg.text and "ជំនួយការប្រើប្រាស់" in msg.text
)
def send_help(message):
  bot.send_message(
      message.chat.id,
      "📌 **របៀបប្រើប្រាស់ Bot នេះ៖**\n"
      "1. **ជជែកសួរនាំផ្ទាល់ (Chat Anything):** អាចសួរគ្រប់សំណួរទូទៅ ឬបច្ចេកវិទ្យា។\n"
      "2. **ផ្ញើ Link ឬ Text:** ដើម្បីពិនិត្យសុវត្ថិភាព (Security Check)។\n"
      "3. **ផ្ញើរូបភាព (Photos):** អាចផ្ញើរូបភាព Screenshot កូដ ឬបញ្ហាផ្សេងៗឱ្យ AI ຊ່ວຍអាន។\n"
      "4. **ប្រើប៊ូតុងខាងក្រោម:** ដើម្បីចូលទៅកាន់មុខងារឯកទេសនីមួយៗយ៉ាងរហ័ស។",
      reply_markup=get_main_menu(),
  )


# 8. ទទួលការផ្ញើរូបភាព (Photos / Screenshots) មកវិភាគ
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
  try:
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    
    bot.reply_to(message, "📸 បានទទួលរូបភាពហើយ! AI កំពុងវិភាគយ៉ាងយកចិត្តទុកដាក់...")

    response = co.chat(
        model="command-a-plus-05-2026",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a versatile, elite AI Assistant capable of helping "
                    "people of all ages, from general knowledge to advanced cybersecurity, "
                    "programming, and technical analysis. The user sent an image. "
                    "Analyze it thoroughly and explain everything clearly, accurately, "
                    "and professionally in natural Khmer language."
                ),
            },
            {
                "role": "user",
                "content": "Please analyze this image and explain what it is.",
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


# 9. ទទួលរាល់សារសន្ទនាទូទៅ វិភាគ Link, File, Code និងចំណេះដឹងគ្រប់ផ្នែក
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    user_input = message.text

    # Prompt កម្រិតខ្ពស់ដែលអាចឆ្លើយតបបានទាំងរឿង IT កម្រិតខ្ពស់ និងចំណេះដឹងទូទៅសម្រាប់គ្រប់វ័យ
    system_prompt = (
        "You are an elite, world-class AI Assistant designed to serve people of all ages "
        "while acting as a personal technical powerhouse for an IT/Cybersecurity student. "
        "You possess deep expertise in:\n"
        "1. Cybersecurity, Ethical Hacking, Networking, Programming, and Device Security (PC, Mobile, Hardware).\n"
        "2. General Knowledge, science, history, health, daily life advice, education, and general inquiries for all ages.\n"
        "When the user sends a Link, URL, Code, or text, analyze it deeply for security threats, phishing risks, bugs, or factual correctness. "
        "If checking a link or file safety, explicitly state whether it is SAFE or DANGEROUS, giving clear, factual reasons. "
        "Always reply in clear, professional, warm, and natural Khmer language, blending precise technical terms when necessary."
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