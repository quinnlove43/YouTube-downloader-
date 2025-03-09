import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TOKEN = os.getenv("TOKEN")  # Use environment variable for security

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Download 1080p", callback_data="1080p"),
         InlineKeyboardButton("Download 4K", callback_data="4k")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Send me a YouTube link:", reply_markup=reply_markup)

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    quality = query.data
    url = context.user_data.get("url")

    if not url:
        await query.edit_message_text("Please send a YouTube link first!")
        return

    await query.edit_message_text("Downloading...")

    ydl_opts = {
        "format": "bestvideo[height={}]+bestaudio/best".format(2160 if quality == "4k" else 1080),
        "outtmpl": "downloads/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    await query.message.reply_document(document=open(file_path, "rb"))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
