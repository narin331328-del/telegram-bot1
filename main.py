import os
import cohere
import telebot
from telebot import types

# ##########################################
# # CONFIG: ព័ត៌មានសម្ងាត់ និងការតភ្ជាប់ API
# ##########################################
TELEGRAM_BOT_TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"
COHERE_API_KEY = "TIavwumKg3mGWOEExWEMshojYT3svthAX1tCH8q"

try:
    co = cohere.ClientV2(api_key=COHERE_API_KEY)
except Exception as e:
    print(f"Cohere Init Error: {e}")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ##########################################
# # HELPER_FUNCTION: សម្រាប់ផ្ញើសារវែងៗ
# ##########################################
def send_long_message(chat_id, text, reply_markup=None):
    max_length = 4000
    if len(text) <= max_length:
        try:
            bot.send_message(chat_id, text, reply_markup=reply_markup, parse_type=None)
        except Exception:
            bot.send_message(chat_id, text, reply_markup=reply_markup)
    else:
        parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        for index, part in enumerate(parts):
            markup = reply_markup if index == len(parts) - 1 else None
            try:
                bot.send_message(chat_id, part, reply_markup=markup, parse_type=None)
            except Exception:
                bot.send_message(chat_id, part, reply_markup=markup)

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("🛡 Ethical Hacking & Security")
    item2 = types.KeyboardButton("🌐 Networking & Cisco")
    item3 = types.KeyboardButton("💻 Programming & Code Debug")
    item4 = types.KeyboardButton("🧠 ចំណេះដឹងបច្ចេកវិទ្យាទូទៅ")
    markup.add(item1, item2, item3, item4)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "សួស្តី លោក/លោកស្រី! ខ្ញុំជា AI ជំនួយការផ្នែក IT និង Cybersecurity របស់អ្នក។ តើថ្ងៃនេះចង់ឱ្យខ្ញុំជួយអ្វីខ្លះ?",
        reply_markup=get_main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    user_input = message.text
    try:
        system_prompt = (
            "អ្នកគឺជាជំនួយការ AI ដ៏ជំនាញផ្នែក IT Networking និង Cybersecurity ។ "
            "ត្រូវប្រើប្រាស់ភាសាខ្មែរឱ្យបានត្រឹមត្រូវតាមស្ដង់ដារ អក្ខរាវិរុទ្ធច្បាស់លាស់ "
            "និងងាយយល់បំផុត ដោយ blending precise technical terms when necessary. "
            "Do NOT use broken markdown symbols that break telegram formatting."
        )

        response = co.chat(
            model="command-a-plus-05-2026",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )

        reply_text = ""
        # ទាញយកទិន្នន័យពី ClientV2 របស់ Cohere យ៉ាងមានសុវត្ថិភាព
        if response and hasattr(response, "message") and response.message:
            if hasattr(response.message, "content") and response.message.content:
                content = response.message.content
                if isinstance(content, list):
                    for item in content:
                        if hasattr(item, "text"):
                            reply_text += item.text
                        elif isinstance(item, dict) and "text" in item:
                            reply_text += item["text"]
                elif isinstance(content, str):
                    reply_text = content

        if not reply_text:
            reply_text = str(response) # fallback បើទម្រង់ទិន្នន័យខុសបន្តិចបន្តួច

        send_long_message(
            message.chat.id,
            reply_text if reply_text else "⚠️ សូមអភ័យទោស ប្រព័ន្ធមិនទាន់ទទួលបានទិន្នន័យឆ្លើយតប។",
            reply_markup=get_main_menu(),
        )
    except Exception as e:
        send_long_message(
            message.chat.id,
            f"⚠️ កំហុសបច្ចេកទេស (Error): {str(e)}",
            reply_markup=get_main_menu(),
        )

# ##########################################
# # RUN BOT (កែសម្រួលចំណុចខុស `__name__` ត្រង់នេះ)
# ##########################################
if __name__ == "__main__":
    set_bot_commands = lambda b: None # Function placeholder ការពារ Error ពេលអត់មាន
    print("Bot is running stably without Markdown parse errors...")
    bot.infinity_polling(skip_pending=True)
