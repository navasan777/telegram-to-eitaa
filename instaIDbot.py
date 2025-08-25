import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# ======== تنظیمات ربات ========
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# ======== تابع گرفتن User ID از اینستاگرام ========
def get_instagram_user_id(input_text):
    try:
        # اگر لینک بود فقط یوزرنیم رو جدا کن
        if "instagram.com" in input_text:
            username = input_text.rstrip("/").split("/")[-1]
        else:
            username = input_text

        url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            user_id = data['graphql']['user']['id']
            return user_id
        else:
            return None
    except:
        return None

# ======== دستورات ربات ========
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "سلام! لینک یا یوزرنیم اینستاگرام رو برام بفرست تا User ID عددیش رو بهت بدم."
    )

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    user_id = get_instagram_user_id(text)
    if user_id:
        update.message.reply_text(f"User ID عددی پیج: {user_id}")
    else:
        update.message.reply_text("متأسفم، نتونستم پیدا کنم. یوزرنیم یا لینک رو درست بفرست.")

# ======== اجرای ربات ========
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
