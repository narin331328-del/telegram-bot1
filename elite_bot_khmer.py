import telebot
from telebot import types
from google import generativeai as genai

# ដាក់ Token និង API Key របស់អ្នកស្រេចក្នុងនេះផ្ទាល់តែម្ដង
TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
GEMINI_API_KEY = "AQ.Ab8RN6JN-EEX1iyIyWjQtLbATGHBhDSQ0BWs5F39mOASDghSjA"

# Config Gemini API
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ១. បង្កើតពាក្យបញ្ជា /start ជាមួយប៊ូតុង Menu ខាងក្រោម
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("💡 ជំនួយ (Help)")
    item2 = types.KeyboardButton("🤖 អំពីខ្ញុំ (About)")
    markup.add(item1, item2)
    
    bot.reply_to(message, "សួស្តី! ខ្ញុំជា AI Bot របស់អ្នក។ តើខ្ញុំអាចជួយអ្វីអ្នកថ្ងៃនេះ?", reply_markup=markup)

# ២. កំណត់ការឆ្លើយតបពេលអ្នកចុចប៊ូតុង ឬផ្ញើសារមក
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    try:
        if text == "💡 ជំនួយ (Help)":
            bot.reply_to(message, "អ្នកអាចសាកសួររាល់សំណួរ ឬបញ្ជាផ្សេងៗទៅកាន់ខ្ញុំបានដោយសេរី!")
        elif text == "🤖 អំពីខ្ញុំ (About)":
            bot.reply_to(message, "ខ្ញុំជា Telegram Bot ដែលขับเคลื่อนដោយ Google Gemini AI!")
        else:
            # ផ្ញើសារទៅសួរ Gemini AI បើមិនមែនជាប៊ូតុង
            response = model.generate_content(text)
            bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")

if __name__ == "__main__":
    print("Bot is running with built-in keys...")
    bot.infinity_polling()