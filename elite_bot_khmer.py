import telebot
from telebot import types
from groq import Groq

TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

SYSTEM_PROMPT = """
អ្នកគឺជាជំនួយការ AI ដ៏ជំនាញផ្នែក IT Networking និង Cybersecurity (Ethical Hacker)។
- ត្រូវប្រើប្រាស់ភាសាខ្មែរឱ្យបានត្រឹមត្រូវ ច្បាស់លាស់ ស្ដង់ដារ និងងាយយល់។
- ពេលនិយាយជាមួយអ្នកប្រើប្រាស់ ត្រូវហៅថា "លោក/លោកស្រី" ឱ្យបានសមរម្យ។
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

@bot.message_handler(commands=['status'])
def send_status(message):
    bot.reply_to(message, "ស្ថានភាពប្រព័ន្ធរបស់ Bot គឺកំពុងដំណើរការធម្មតា ១០០% (Active) និងមានសុវត្ថិភាពល្អប្រសើរ។ តើលោក/លោកស្រីចង់ឱ្យខ្ញុំពិនិត្យអ្វីបន្ថែមទៀតទេ?")

@bot.message_handler(commands=['scan'])
def send_scan_info(message):
    bot.reply_to(message, "មុខងារ Scan កំពុងរួចរាល់ជាស្រេច! សូមផ្ញើតំណភ្ជាប់ (Link) រូបភាព ឬឯកសារមកកាន់ទីនេះ ខ្ញុំនឹងជួយលោក/លោកស្រីវិភាគរកភាពខុសប្រក្រតី និងសុវត្ថិភាពជូន។")

@bot.message_handler(content_types=['photo', 'document'])
def handle_files(message):
    bot.reply_to(message, "🔍 ខ្ញុំបានទទួលឯកសារ/រូបភាពរបស់លោក/លោកស្រីហើយ។ ក្នុងនាមជាជំនួយការ Cybersecurity, ខ្ញុំសូមណែនាំថា៖ រាល់ឯកសារមិនស្គាល់ប្រភព គឺគួរតែប្រុងប្រយ័ត្នខ្ពស់ ព្រោះវាអាចជា Phishing ឬ Malware បង្កប់។ តើលោក/លោកស្រីចង់ឱ្យខ្ញុំជួយវិភាគចំណុចណាមួយបន្ថែមទេ?")

# ⚙️ កន្លែងសម្រាប់កែប្រែអត្ថបទស្វាគមន៍ពេលមានគេវាយពាក្យ Hi ឬ Hello តាមចិត្តអ្នក!
@bot.message_handler(func=lambda message: message.text and message.text.lower() in ['hi', 'hello', 'សួស្តី', 'хо'])
def handle_greetings(message):
    # 👇 អ្នកអាចដូរអត្ថបទនៅក្នុងសញ្ញា quotation mark ("...") ខាងក្រោមនេះជាអត្ថបទរបស់អ្នកផ្ទាល់
    custom_greeting_text = "សួស្តី លោក/លោកស្រី! ខ្ញុំគឺជាជំនួយការផ្ទាល់ខ្លួនរបស់អ្នក។ តើថ្ងៃនេះមានបញ្ហាផ្នែក IT ឬ Cybersecurity អ្វីខ្លះដែលចង់ឱ្យខ្ញុំជួយដោះស្រាយ?"
    bot.reply_to(message, custom_greeting_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    try:
        if text == "🛡 Ethical Hacking & Security":
            bot.reply_to(message, "ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចដើម្បីជួយពិភាក្សាជូនលោក/លោកស្រីអំពី Penetration Testing, OWASP Top 10, Nmap scanning, Metasploit, Linux Security, និងការការពារប្រព័ន្ធ (Defensive Security)។")
        elif text == "🌐 Networking & Cisco":
            bot.reply_to(message, "ខ្ញុំអាចជួយលោក/លោកស្រីពន្យល់ពី Subnetting, OSI Model, TCP/IP, VLAN, Routing Protocols, និង Cisco Command Line Configurations។")
        elif text == "💻 Programming & Code Debug":
            bot.reply_to(message, "សូមផ្ញើ Code របស់លោក/លោកស្រីមកទីនេះ (Python, Bash, C++, JavaScript...) ខ្ញុំនឹងជួយ Debug និងពិនិត្យរក Error ជូន!")
        elif text == "🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ (គ្រប់វ័យ)":
            bot.reply_to(message, "មុខងារនេះគឺសម្រាប់រៀបចំចំណេះដឹងទូទៅអំពីបច្ចេកវិទ្យា SmartPhone អ៊ីនធឺណិត និងសុវត្ថិភាពអនឡាញ ដែលងាយយល់បំផុតសម្រាប់គ្រប់វ័យ។ តើលោក/លោកស្រីចង់ដឹងពីអ្វី?")
        elif text == "🔍 Scan/Analyze Link or Text":
            bot.reply_to(message, "សូមផ្ញើតំណភ្ជាប់ (Link) ឬ Log មក ខ្ញុំនឹងជួយលោក/លោកស្រីពិនិត្យមើលភាពខុសប្រក្រតី ឬសុវត្ថិភាពជូន!")
        else:
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
    print("Bot is running with custom greeting support...")
    bot.infinity_polling()