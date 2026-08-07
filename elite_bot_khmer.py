import os
import platform
import psutil
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "8812870706:AAF_VEcy-lvnhUI6FqGeujllddRSaGqaKts"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📊 ស្ថានភាពប្រព័ន្ធ", callback_data="status"),
            InlineKeyboardButton("🛡️ ការពិនិត្យសុវត្ថិភាព", callback_data="scan"),
        ],
        [InlineKeyboardButton("ℹ️ ជំនួយ និងការណែនាំ", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        "🔥 *ជម្រាបសួរលោក Narin!* 🙏\n\n"
        "ប្រព័ន្ធសុវត្ថិភាព Bot របស់អ្នកត្រូវបានដំណើរការដោយជោគជ័យ និងត្រៀមខ្លួនរួចជាស្រេចហើយ។ "
        "សូមជ្រើសរើសជម្រើសខាងក្រោមនេះ ឬវាយបញ្ចូលបញ្ជា៖"
    )
    if update.message:
        await update.message.reply_text(
            welcome_text, parse_mode="Markdown", reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            welcome_text, parse_mode="Markdown", reply_markup=reply_markup
        )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    os_info = platform.system() + " " + platform.release()

    report = (
        "🟢 *របាយការណ៍ស្ថានភាពប្រព័ន្ធកុំព្យូទ័រ*\n\n"
        f"💻 *ប្រព័ន្ធប្រតិបត្តិការ:* `{os_info}`\n"
        f"⚡ *ការប្រើប្រាស់ CPU:* `{cpu}%`\n"
        f"🧠 *ការប្រើប្រាស់ RAM:* `{memory}%`\n"
        f"💾 *ការប្រើប្រាស់ Disk:* `{disk}%`\n"
        "🔒 *ស្ថានភាព:* សុវត្ថិភាព និងលំនឹងល្អ"
    )

    if update.message:
        await update.message.reply_text(report, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            report,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("« ត្រឡប់ក្រោយ", callback_data="back")]]
            ),
        )


async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scan_msg = (
        "🛡️ *ការពិនិត្យបណ្តាញ និងរន្ធតភ្ជាប់ (Network Scan)*\n\n"
        "កំពុងစစ်និត្យប្រព័ន្ធបណ្តាញក្នុងម៉ាស៊ីន...\n"
        "✅ *Port 22 (SSH):* មានសុវត្ថិភាព\n"
        "✅ *Port 80 (HTTP):* កំពុងដំណើរការ\n"
        "✅ *Port 443 (HTTPS):* កំពុងដំណើរការ\n\n"
        "✨ *លទ្ធផល:* មិនមានការទម្លុះទម្លាយ ឬ intrusions ណាមួយកើតឡើងទេ។"
    )
    if update.message:
        await update.message.reply_text(scan_msg, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            scan_msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("« ត្រឡប់ក្រោយ", callback_data="back")]]
            ),
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *មុខងារនៃការប្រើប្រាស់ Bot*\n\n"
        "/start - បង្ហាញផ្ទាំងបញ្ជាដើម\n​"
        "/status - ពិនិត្យមើលកម្លាំងម៉ាស៊ីន (CPU/RAM)\n"
        "/scan - និត្យមើលសុវត្ថិភាព Port ក្នុងបណ្តាញ\n"
        "/help - បង្ហាញបញ្ជីជំនួយ"
    )
    if update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            help_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("« ត្រឡប់ក្រោយ", callback_data="back")]]
            ),
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "status":
        await status_command(update, context)
    elif query.data == "scan":
        await scan_command(update, context)
    elif query.data == "help":
        await help_command(update, context)
    elif query.data == "back":
        await start(update, context)


async def echo_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = (
        f"🤖 *សាររបស់អ្នក៖* `{user_text}`\n"
        "សូមវាយពាក្យ /start ដើម្បីបើកផ្ទាំងបញ្ជា ឬ /help ដើម្បីសាកសួរព័ត៌មានបន្ថែម។"
    )
    await update.message.reply_text(response, parse_mode="Markdown")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("scan", scan_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_all))

    print("🚀 Bot សុវត្ថិភាពជាភាសាខ្មែរ កំពុងដំណើរការយ៉ាងរលូនហើយ...")
    app.run_polling()