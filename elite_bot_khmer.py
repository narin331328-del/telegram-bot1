import telebot
from telebot import types
from groq import Groq

# ព័ត៌មានសម្ងាត់សម្រាប់ Bot និង API
TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
GROQ_API_KEY = "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"

# កំណត់ការតភ្ជាប់
client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("💡 ជំនួយ (Help)")
    item2 = types.KeyboardButton("🤖 អំពីខ្ញុំ (About)")
    markup.add(item1, item2)
    bot.reply_to(message, "សួស្តី! ខ្ញុំជា AI Bot របស់អ្នក។ តើខ្ញុំអាចជួយអ្វីអ្នកថ្ងៃនេះ?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    try:
        if text == "💡 ជំនួយ (Help)":
            bot.reply_to(message, "អ្នកអាចសាកសួររាល់សំណួរ ឬបញ្ជាផ្សេងៗទៅកាន់ខ្ញុំបានដោយសេរី!")
        elif text == "🤖 អំពីខ្ញុំ (About)":
            bot.reply_to(message, "ខ្ញុំជា Telegram Bot ដែលដោយ Groq AI (Llama 3.1)!")
        else:
            # ហៅប្រើម៉ូដែលថ្មី និងដំណើរការប្រក្រតីរបស់ Groq
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": text}],
                model="llama-3.1-8b-instant",
            )
            bot.reply_to(message, chat_completion.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"មានបញ្ហាបន្តិច៖ {str(e)}")

if __name__ == "__main__":
    print("Bot is running successfully with Groq AI...")
    bot.infinity_polling()