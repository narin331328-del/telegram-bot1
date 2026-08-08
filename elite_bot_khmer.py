import telebot
from telebot import types
from groq import Groq

TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# System Prompt សម្រាប់ជំនួយការ IT, Cybersecurity និងចំណេះដឹងបច្ចេកវិទ្យាទូទៅគ្រប់វ័យ
SYSTEM_PROMPT = """
អ្នកគឺជាជំនួយការ AI ដ៏ជំនាញមួយរូបដែលមានឯកទេសខាងផ្នែក បណ្តាញកុំព្យូទ័រ (IT Networking), ការសរសេរកម្មវិធី (Software Programming), សុវត្ថិភាពអនឡាញ (Cybersecurity), និងចំណេះដឹងបច្ចេកវិទ្យាទូទៅដែលស័ក្តិសមសម្រាប់មនុស្សគ្រប់វ័យ។
- ត្រូវផ្តល់ការពន្យល់ឱ្យបានច្បាស់លាស់ ត្រឹមត្រូវ និងងាយយល់ជានិច្ច។
- ពេលនិយាយជាមួយអ្នកប្រើប្រាស់ ត្រូវប្រើពាក្យគោរពហៅថា "លោក/លោកស្រី" ឱ្យបានត្រឹមត្រូវ និងសមរម្យ។
- នៅពេលឆ្លើយសំណួរបច្ចេកវិទ្យាទូទៅ ត្រូវប្រើឧទាហរណ៍ប្រៀបធៀបងាយៗ និងភាសាខ្មែរច្បាស់លាស់ ងាយយល់។
- នៅពេលឆ្លើយសំណួរកម្រិតខ្ពស់ផ្នែក IT/Cybersecurity ត្រូវផ្តល់នូវការយល់ដឹងស៊ីជម្រៅផ្នែកបច្ចេកទេស, គោលគំនិតនៃការវាយប្រហារបែបសីលធម៌ (Ethical Hacking), និងយុទ្ធសាស្ត្រការពារប្រព័ន្ធបច្ចេកវិទ្យា (Defensive Strategies)។
- ត្រូវឆ្លើយតបជាភាសាខ្មែរច្បាស់លាស់ ដោយលាយឡំជាមួយនឹងពាក្យបច្ចេកទេសត្រឹមត្រូវនៅកន្លែងណាដែលចាំបាច់។
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("🛡 Ethical Hacking & Security")
    item2 = types.KeyboardButton("🌐 Networking & Cisco")
    item3 = types.KeyboardButton("💻 Programming & Code Debug")
    item4 = types.KeyboardButton("🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ (គ្រប់វ័យ)")
    item5 = types.KeyboardButton("🔍 Scan/Analyze Link or Text")
    markup.add(item1, item2, item3, item4, item5)
    bot.reply_to(message, "សួស្តី! ខ្ញុំជា AI ជំនួយការផ្នែក IT, Cybersecurity និងចំណេះដឹងបច្ចេកវិទ្យាទូទៅរបស់អ្នក។ តើចង់ឱ្យខ្ញុំជួយអ្វីថ្ងៃនេះ?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    try:
        if text == "🛡 Ethical Hacking & Security":
            bot.reply_to(message, "ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចដើម្បីជួយពិភាក្សាអំពី Penetration Testing, OWASP Top 10, Nmap scanning, Metasploit, Linux Security, និងការការពារប្រព័ន្ធ (Defensive Security)។")
        elif text == "🌐 Networking & Cisco":
            bot.reply_to(message, "ខ្ញុំអាចជួយពន្យល់ពី Subnetting, OSI Model, TCP/IP, VLAN, Routing Protocols, និង Cisco Command Line Configurations។")
        elif text == "💻 Programming & Code Debug":
            bot.reply_to(message, "សូមផ្ញើ Code មកទីនេះ (Python, Bash, C++, JavaScript...) ខ្ញុំនឹងជួយ Debug និងពិនិត្យរក Error ជូន!")
        elif text == "🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ(គ្រប់វ័យ)":
            bot.reply_to(message, "មុខងារនេះគឺសម្រាប់រៀបចំ ចំណេះដឹងទូទៅអំពីបច្ចេកវិទ្យា SmartPhone អ៊ីនធឺណិត និងសុវត្ថិភាពអនឡាញ ដែលងាយយល់បំផុតសម្រាប់គ្រប់វ័យ។ តើលោក/លោកស្រីចង់ដឹងពីអ្វីផ្សេងទៀតដែរឬទេ?")
        elif text == "🔍 Scan/Analyze Link or Text":
            bot.reply_to(message, "សូមផ្ញើតំណភ្ជាប់ (Link) ឬ Log មក ខ្ញុំនឹងជួយលោក/លោកស្រីពិនិត្យមើលភាពខុសប្រក្រតី ឬសុវត្ថិភាពជូន!")
        else:
            # AI System Prompt
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

if __name__ == "__main__":
    print("Bot is running with General Tech Knowledge & Cyber Security support...")
    bot.infinity_polling()