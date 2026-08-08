import os
import telebot
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_BOT_TOKEN = os.environ.get("8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts")
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6JwQmSSHSrsbOLDy3Fp7wMcjDmwIlxUhUkCcos0DhIVmA")

bot = telebot.TeleBot(8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts)

genai.configure(api_key=AQ.Ab8RN6JwQmSSHSrsbOLDy3Fp7wMcjDmwIlxUhUkCcos0DhIVmA)
ai_model = genai.GenerativeModel("gemini-1.5-flash")

# បង្កើត Menu ជាមួយប៊ូតុង 6 មុខងារសំខាន់ៗ (Best for all devices)
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🛡️ ពិនិត្យសុវត្ថិភាព Link", callback_data="check_link")
    btn2 = InlineKeyboardButton("🔐 ឆែក Password ខ្លាំង/ខ្សោយ", callback_data="check_pass")
    btn3 = InlineKeyboardButton("🌐 ពិនិត្យ IP / Domain", callback_data="ip_lookup")
    btn4 = InlineKeyboardButton("🤖 AI Cybersecurity Expert", callback_data="ai_chat")
    btn5 = InlineKeyboardButton("💡 טיפסការពារខ្លួន (Tips)", callback_data="security_tips")
    btn6 = InlineKeyboardButton("ℹ️ ជំនួយ និងការណែនាំ", callback_data="help_menu")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

# ពេលវាយ /start ឬ /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"🔥 ជម្រាបសួរលោក **{user_name}**! 🙏\n\n"
        "ប្រព័ន្ធសុវត្ថិភាព Bot របស់អ្នកត្រូវបានដំណើរការដោយជោគជ័យ និងត្រៀមខ្លួនរួចជាស្រេចហើយ។\n"
        "សូមជ្រើសរើសជម្រើសខាងក្រោមនេះ ឬផ្ញើសារសួរមកកាន់ខ្ញុំផ្ទាល់៖"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

# จัดการការចុចប៊ូតុង (Inline Button Actions)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "check_link":
        bot.send_message(chat_id, "🔗 សូមផ្ញើ Link (URL) ដែលអ្នកចង់ឆែកសុវត្ថិភាពមកកាន់ទីនេះ ខ្ញុំនឹងវិភាគជូន!")
    elif call.data == "check_pass":
        bot.send_message(chat_id, "🔐 សូមផ្ញើ Password ដែលអ្នកចង់ពិនិត្យកម្រិតសុវត្ថិភាពមក (ឧទាហរណ៍៖ Test@123)")
    elif call.data == "ip_lookup":
        bot.send_message(chat_id, "🌐 សូមផ្ញើលេខ IP Address ឬ Domain Website មកដើម្បីពិនិត្យព័ត៌មានមូលដ្ឋាន។")
    elif call.data == "ai_chat":
        bot.send_message(chat_id, "🤖 លោកអ្នកអាចសាកសួររាល់សំណួរទាក់ទងនឹង Cybersecurity និង Ethical Hacking មកកាន់ខ្ញុំបានដោយសេរី!")
    elif call.data == "security_tips":
        tips = (
            "💡 **គន្លឹះការពារខ្លួនពី Hacker:**\n"
            "1. កុំចុចលើ Link ប្លែកៗដែលមិនស្គាល់ប្រភព។\n"
            "2. បើកប្រព័ន្ធ 2FA (Two-Factor Authentication) គ្រប់គណនីទាំងអស់។\n"
            "3. ប្រើប្រាស់ Password ខុសៗគ្នាសម្រាប់គណនីនីមួយៗ។\n"
            "4. ធ្វើបច្ចុប្បន្នភាព Software ជានិច្ច។"
        )
        bot.send_message(chat_id, tips, parse_mode="Markdown")
    elif call.data == "help_menu":
        bot.send_message(chat_id, "ℹ️ Bot นี้ត្រូវបានបង្កើតឡើងដើម្បីជួយការពារសុវត្ថិភាពប្រព័ន្ធ និងផ្ដល់ចំណេះដឹងផ្នែក Ethical Hacking។ ចុច /start ដើម្បីត្រឡប់ទៅ Menu ដើម។")

# គ្រប់គ្រងរាល់សារដែលអ្នកប្រើប្រាស់វាយចូលមក (Text Messages & AI Analysis)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    chat_id = message.chat.id
    
    # បើមានគេផ្ញើ Link មក
    if "http://" in user_text or "https://" in user_text:
        bot.send_message(chat_id, "🔍 កំពុងធ្វើការវិភាគសុវត្ថិភាពផ្អែកលើ Link នេះតាមរយៈ AI...")
        try:
            prompt = f"Analyze this link/URL for potential phishing, malware, or security risks and give a safety verdict (Safe or Dangerous with reasons): {user_text}"
            response = ai_model.generate_content(prompt)
            bot.send_message(chat_id, f"🛡️ **លទ្ធផលវិភាគសុវត្ថិភាព Link:**\n\n{response.text}", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(chat_id, "⚠️ មានបញ្ហាក្នុងការភ្ជាប់ជាមួយប្រព័ន្ធវិភាគសុវត្ថិភាព!")
    else:
        # សំណួរធម្មតា ឬសំណួរទាក់ទងនឹង Cybersecurity ឆ្លើយតបដោយ AI
        bot.send_chat_action(chat_id, 'typing')
        try:
            prompt = f"You are an expert Cybersecurity and Ethical Hacking Assistant. Answer this question clearly, professionally, and securely: {user_text}"
            response = ai_model.generate_content(prompt)
            bot.send_message(chat_id, response.text)
        except Exception as e:
            bot.send_message(chat_id, "⚠️ មានបញ្ហាក្នុងការភ្ជាប់ជាមួយ AI System!")

print("Bot is running...")
bot.infinity_polling()
