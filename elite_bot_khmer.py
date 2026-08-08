import telebot
from telebot import types
import anthropic
import os

# ##########################################
# # 1. SETUP API & CLIENTS
# ##########################################
TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"

# យក Key មកទាញចេញពី Railway Variables ដោយសុវត្ថិភាព
ANTHROPIC_API_KEY = os.environ.get("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", "បញ្ចូល_API_Key_របស់អ្នកនៅទីនេះ_ប្រសិនបើមិនប្រើ_Railway")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ##########################################
# # 2. SYSTEM PROMPT (ច្បាប់បញ្ជា AI ឱ្យប្រើភាសាខ្មែរស្ដង់ដារ)
# ##########################################
SYSTEM_PROMPT = """
អ្នកគឺជាជំនួយការ AI ដ៏ជំនាញផ្នែក IT Networking និង Cybersecurity (Ethical Hacker)។
- ត្រូវប្រើប្រាស់ភាសាខ្មែរឱ្យបានត្រឹមត្រូវតាមស្ដង់ដារ អក្ខរាវិរុទ្ធច្បាស់លាស់ និងងាយយល់បំផុត។
- ពេលនិយាយជាមួយអ្នកប្រើប្រាស់ ត្រូវហៅថា "លោក/លោកស្រី" ឱ្យបានសមរម្យជានិច្ច។
- ពេលវិភាគតំណភ្ជាប់ (Link), រូបភាព (Image), កូដ (Code) ឬសំណួរផ្សេងៗ ត្រូវពន្យល់ជាភាសាខ្មែរឱ្យបានត្រឹមត្រូវនិងស៊ីជម្រៅ។
"""

# ##########################################
# # 3. COMMAND /start (ម៉ឺនុយប៊ូតុងចុចចាប់ផ្តើម)
# ##########################################
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("🛡 Ethical Hacking & Security")
    item2 = types.KeyboardButton("🌐 Networking & Cisco")
    item3 = types.KeyboardButton("💻 Programming & Code Debug")
    item4 = types.KeyboardButton("🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ (គ្រប់វ័យ)")
    markup.add(item1, item2, item3, item4)
    bot.reply_to(message, "សួស្តី លោក/លោកស្រី! ខ្ញុំជា AI (Claude 3.5 Sonnet) ជំនួយការផ្នែក IT និង Cybersecurity របស់អ្នក។ តើថ្ងៃនេះចង់ឱ្យខ្ញុំជួយអ្វីខ្លះ?", reply_markup=markup)

# ##########################################
# # 4. COMMAND /status (ពិនិត្យស្ថានភាពប្រព័ន្ធ)
# ##########################################
@bot.message_handler(commands=['status'])
def send_status(message):
    bot.reply_to(message, "ស្ថានភាពប្រព័ន្ធរបស់ Bot (Claude 3.5 Sonnet) គឺកំពុងដំណើរការធម្មតា ១០០% (Active) និងមានសុវត្ថិភាពល្អប្រសើរ។")

# ##########################################
# # 5. MAIN MESSAGE HANDLER (ប្រើ Claude 3.5 Sonnet)
# ##########################################
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    try:
        if text == "🛡 Ethical Hacking & Security":
            bot.reply_to(message, "ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចដើម្បីជួយពិភាក្សាជូនលោក/លោកស្រីអំពី Penetration Testing, OWASP Top 10, Nmap scanning, និង Linux Security។")
        elif text == "🌐 Networking & Cisco":
            bot.reply_to(message, "ខ្ញុំអាចជួយលោក/លោកស្រីពន្យល់ពី Subnetting, OSI Model, TCP/IP, VLAN និង Cisco Configurations។")
        elif text == "💻 Programming & Code Debug":
            bot.reply_to(message, "សូមផ្ញើ Code របស់លោក/លោកស្រីមកទីនេះ ខ្ញុំនឹងជួយ Debug និងពិនិត្យរក Error ជូន!")
        elif text == "🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ (គ្រប់វ័យ)":
            bot.reply_to(message, "មុខងារនេះសម្រាប់រៀបចំចំណេះដឹងទូទៅអំពីបច្ចេកវិទ្យា SmartPhone អ៊ីនធឺណិត និងសុវត្ថិភាពអនឡាញ។")
        else:
            # បញ្ជូនទិន្នន័យទៅកាន់ Claude 3.5 Sonnet
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": text}
                ]
            )
            bot.reply_to(message, response.content[0].text)
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")

# ##########################################
# # 6. RUN BOT
# ##########################################
if __name__ == "__main__":
    print("Bot is running with Claude 3.5 Sonnet...")
    bot.infinity_polling()