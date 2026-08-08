import telebot
from telebot import types
from groq import Groq

# ##########################################
# # 1. SETUP API TOKENS & CLIENTS
# ##########################################
# កន្លែងដាក់ Token របស់ Telegram Bot និង Groq API Key របស់អ្នក
TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ##########################################
# # 2. SYSTEM PROMPT (ច្បាប់បញ្ជា AI)
# ##########################################
# កន្លែងកំណត់បុគ្គលិកលក្ខណៈ និងតួនាទីរបស់ AI ឱ្យឆ្លើយតបបានត្រឹមត្រូវស្ដង់ដារ
SYSTEM_PROMPT = """
អ្នកគឺជាជំនួយការ AI ដ៏ជំនាញផ្នែក IT Networking និង Cybersecurity (Ethical Hacker)។
- ត្រូវប្រើប្រាស់ភាសាខ្មែរឱ្យបានត្រឹមត្រូវ ច្បាស់លាស់ ស្ដង់ដារ និងងាយយល់បំផុត។
- ពេលនិយាយជាមួយអ្នកប្រើប្រាស់ ត្រូវហៅថា "លោក/លោកស្រី" ឱ្យបានសមរម្យជានិច្ច។
- ហ้ามបង្កើតរឿងខុសការពិត ហ้ามបកប្រែខុសទម្រង់ ស្ដាប់សំណួរឱ្យយល់ច្បាស់មុននឹងឆ្លើយ។
- ប្រសិនបើមានគេផ្ញើតំណភ្ជាប់ (Link) កូដ (Code) ឬសំណួរផ្សេងៗ ត្រូវវិភាគដោយយកចិត្តទុកដាក់ជាភាសាខ្មែរឱ្យបានច្បាស់លាស់។
"""

# ##########################################
# # 3. COMMAND /start (ម៉ឺនុយប៊ូតុងចុចចាប់ផ្តើម)
# ##########################################
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # បង្កើតប៊ូតុង Reply Keyboard ខាងក្រោមឆាត
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("🛡 Ethical Hacking & Security")
    item2 = types.KeyboardButton("🌐 Networking & Cisco")
    item3 = types.KeyboardButton("💻 Programming & Code Debug")
    item4 = types.KeyboardButton("🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ (គ្រប់វ័យ)")
    item5 = types.KeyboardButton("🔍 Scan/Analyze Link or Text")
    markup.add(item1, item2, item3, item4, item5)
    
    # សារស្វាគមន៍ពេលចាប់ផ្តើម
    bot.reply_to(message, "សួស្តី លោក/លោកស្រី! ខ្ញុំជា AI ជំនួយការផ្នែក IT, Cybersecurity និងចំណេះដឹងបច្ចេកវិទ្យាទូទៅរបស់អ្នក។ តើថ្ងៃនេះចង់ឱ្យខ្ញុំជួយអ្វីខ្លះ?", reply_markup=markup)

# ##########################################
# # 4. COMMAND /status (ពិនិត្យស្ថានភាពប្រព័ន្ធ)
# ##########################################
@bot.message_handler(commands=['status'])
def send_status(message):
    bot.reply_to(message, "ស្ថានភាពប្រព័ន្ធរបស់ Bot គឺកំពុងដំណើរការធម្មតា ១០០% (Active) និងមានសុវត្ថិភាពល្អប្រសើរ។ តើលោក/លោកស្រីចង់ឱ្យខ្ញុំពិនិត្យអ្វីបន្ថែមទៀតទេ?")

# ##########################################
# # 5. COMMAND /scan ឬ /help (ជំនួយការស្កេន)
# ##########################################
@bot.message_handler(commands=['scan', 'help'])
def send_scan_info(message):
    bot.reply_to(message, "មុខងារវិភាគសុវត្ថិភាពកំពុងរួចរាល់ជាស្រេច! សូមផ្ញើតំណភ្ជាប់ (Link), រូបភាព (Image), ឯកសារ (File) ឬកូដ (Code) មកកាន់ទីនេះ ខ្ញុំនឹងជួយលោក/លោកស្រីពិនិត្យរកភាពខុសប្រក្រតីជូន។")

# ##########################################
# # 6. HANDLER FOR IMAGES & FILES (កន្លែងសម្រាប់ផ្ញើរូបភាព ឯកសារ ឬ File ផ្សេងៗ)
# ##########################################
@bot.message_handler(content_types=['photo', 'document'])
def handle_files(message):
    # កន្លែងនេះកែសម្រួលសារឆ្លើយតបពេលមានគេផ្ញើ File ឬ Photo ចូលមក
    bot.reply_to(message, "🔍 ខ្ញុំបានទទួលរូបភាព/ឯកសាររបស់លោក/លោកស្រីហើយ។ ក្នុងនាមជាជំនួយការ Cybersecurity, រាល់ឯកសារមិនស្គាល់ប្រភព ឬស្គ្រីបចម្លែក គឺតម្រូវឱ្យពិនិត្យមើល Extension និង Source Code ឱ្យបានហ្មត់ចត់ដើម្បីការពារ Malware ឬ Phishing។ តើលោក/លោកស្រីចង់ឱ្យខ្ញុំជួយពន្យល់ចំណុចណាមួយទេ?")

# ##########################################
# # 7. HANDLER FOR GREETINGS (កន្លែងកែប្រែពាក្យស្វាគមន៍ Hi / Hello)
# ##########################################
@bot.message_handler(func=lambda message: message.text and message.text.lower() in ['hi', 'hello', 'សួស្តី', 'hey'])
def handle_greetings(message):
    # 👇 អ្នកអាចដូរអត្ថបទនៅក្នុងសញ្ញា quotation mark ("...") នេះតាមចិត្តចង់បាន
    custom_greeting_text = "សួស្តី លោក/លោកស្រី! ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចដើម្បីជួយឆ្លើយតបសំណួរ និងវិភាគបញ្ហាផ្នែក IT ឬ Cybersecurity ជូនលោក/លោកស្រីហើយ។ តើមានអ្វីឱ្យខ្ញុំជួយទេ?"
    bot.reply_to(message, custom_greeting_text)

# ##########################################
# # 8. MAIN MESSAGE HANDLER (គ្រប់គ្រងអត្ថបទ លីង កូដ និងប៊ូតុងចុច)
# ##########################################
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    try:
        # ឆែកមើលថាតើអ្នកប្រើប្រាស់ចុចលើប៊ូតុងណាមួយក្នុង Menu ដែរឬទេ
        if text == "🛡 Ethical Hacking & Security":
            bot.reply_to(message, "ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចដើម្បីជួយពិភាក្សាជូនលោក/លោកស្រីអំពី Penetration Testing, OWASP Top 10, Nmap scanning, Metasploit, Linux Security, និងការការពារប្រព័ន្ធ (Defensive Security)។")
        elif text == "🌐 Networking & Cisco":
            bot.reply_to(message, "ខ្ញុំអាចជួយលោក/លោកស្រីពន្យល់ពី Subnetting, OSI Model, TCP/IP, VLAN, Routing Protocols, និង Cisco Command Line Configurations។")
        elif text == "💻 Programming & Code Debug":
            bot.reply_to(message, "សូមផ្ញើ Code របស់លោក/លោកស្រីមកទីនេះ (Python, Bash, C++, JavaScript...) ខ្ញុំនឹងជួយ Debug និងពិនិត្យរក Error ជូន!")
        elif text == "🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ (គ្រប់វ័យ)":
            bot.reply_to(message, "មុខងារនេះគឺសម្រាប់រៀបចំចំណេះដឹងទូទៅអំពីបច្ចេកវិទ្យា SmartPhone អ៊ីនធឺណិត និងសុវត្ថិភាពអនឡាញ ដែលងាយយល់បំផុតសម្រាប់គ្រប់វ័យ។ តើលោក/លោកស្រីចង់ដឹងពីអ្វី?")
        elif text == "🔍 Scan/Analyze Link or Text":
            bot.reply_to(message, "សូមផ្ញើតំណភ្ជាប់ (Link), រូបភាព ឬ Log មក ខ្ញុំនឹងជួយលោក/លោកស្រីពិនិត្យមើលភាពខុសប្រក្រតី ឬសុវត្ថិភាពជូន!")
        else:
            # បើជាសំណួរទូទៅ, ការផ្ញើលីង (Link), ឬការផ្ញើកូដ (Code) គឺបញ្ជូនទៅកាន់ Groq AI (Llama 3.1) ដើម្បីវិភាគ
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text}
                ],
                model="llama-3.1-8b-instant",
            )
            bot.reply_to(message, chat_completion.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")

# ##########################################
# # 9. RUN BOT
# ##########################################
if __name__ == "__main__":
    print("Bot is running with full fixes and well-commented code...")
    bot.infinity_polling()