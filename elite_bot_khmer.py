import telebot
from telebot import types
import google.generativeai as genai
import os

# ##########################################
# # 1. SETUP API & CLIENTS
# ##########################################
TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"

# យក Key មកទាញពី Environment Variables ដោយសុវត្ថិភាព ឬដាក់ជំនួសកន្លែងនេះ
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "ដាក់_API_Key_របស់អ្នកនៅទីនេះ_ប្រសិនបើមិនប្រើ_Railway")

genai.configure(api_key=GOOGLE_API_KEY)

# ជ្រើសរើស Model Gemini
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="""
    អ្នកគឺជាជំនួយការ AI ដ៏ជំនាញផ្នែក IT Networking និង Cybersecurity។
    - ត្រូវប្រើប្រាស់ភាសាខ្មែរឱ្យបានត្រឹមត្រូវតាមស្ដង់ដារ អក្ខរាវិរុទ្ធច្បាស់លាស់ និងងាយយល់បំផុត។
    - ពេលនិយាយជាមួយអ្នកប្រើប្រាស់ ត្រូវហៅថា "លោក/លោកស្រី" ឱ្យបានសមរម្យជានិច្ច។
    """
)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ##########################################
# # 2. COMMAND /start
# ##########################################
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("🛡 Ethical Hacking & Security")
    item2 = types.KeyboardButton("🌐 Networking & Cisco")
    item3 = types.KeyboardButton("💻 Programming & Code Debug")
    item4 = types.KeyboardButton("🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ (គ្រប់វ័យ)")
    markup.add(item1, item2, item3, item4)
    bot.reply_to(message, "សួស្តី លោក/លោកស្រី! ខ្ញុំជា AI (Gemini) ជំនួយការផ្នែក IT និង Cybersecurity របស់អ្នក។ តើថ្ងៃនេះចង់ឱ្យខ្ញុំជួយអ្វីខ្លះ?", reply_markup=markup)

# ##########################################
# # 3. MAIN MESSAGE HANDLER (ប្រើ Gemini AI)
# ##########################################
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    try:
        if text == "🛡 Ethical Hacking & Security":
            bot.reply_to(message, "ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចដើម្បីជួយពិភាក្សាអំពី Penetration Testing, OWASP Top 10, Nmap, និង Security។")
        elif text == "🌐 Networking & Cisco":
            bot.reply_to(message, "ខ្ញុំអាចជួយពន្យល់ពី Subnetting, OSI Model, TCP/IP, VLAN និង Cisco Configurations។")
        elif text == "💻 Programming & Code Debug":
            bot.reply_to(message, "សូមផ្ញើ Code មកទីនេះ ខ្ញុំនឹងជួយ Debug និងរក Error ជូន!")
        else:
            response = model.generate_content(text)
            bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")

# ##########################################
# # 4. RUN BOT
# ##########################################
if __name__ == "__main__":
    print("Bot is running with Google Gemini...")
    bot.infinity_polling()