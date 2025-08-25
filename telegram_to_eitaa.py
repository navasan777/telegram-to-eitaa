import requests
from telegram.ext import Updater, MessageHandler, Filters

# --- تنظیمات ---
telegram_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
telegram_channel = "@your_private_channel"   # کانال خصوصی تلگرام (ادمینش کن)
eitaa_token = "YOUR_EITAA_BOT_TOKEN"
eitaa_channel = "@your_eitaa_channel"        # کانال خصوصی ایتا (ادمینش کن)

# --- ارسال پیام به ایتا ---
def send_to_eitaa(endpoint, data, files=None):
    url = f"https://eitaayar.ir/api/{eitaa_token}/{endpoint}"
    try:
        r = requests.post(url, data={"chat_id": eitaa_channel, **data}, files=files)
        print("📤 پاسخ ایتا:", r.text)
    except Exception as e:
        print("❌ خطا در ارسال به ایتا:", e)

# --- وقتی پیام جدید در کانال تلگرام بیاد ---
def forward_to_eitaa(update, context):
    msg = update.channel_post
    
    # متن ساده
    if msg.text:
        send_to_eitaa("sendMessage", {"text": msg.text})

    # عکس
    elif msg.photo:
        file = msg.photo[-1].get_file()
        file_path = file.download()
        with open(file_path, 'rb') as f:
            send_to_eitaa("sendPhoto", {"caption": msg.caption or ""}, {"photo": f})

    # ویدیو
    elif msg.video:
        file = msg.video.get_file()
        file_path = file.download()
        with open(file_path, 'rb') as f:
            send_to_eitaa("sendVideo", {"caption": msg.caption or ""}, {"video": f})

    # ویس
    elif msg.voice:
        file = msg.voice.get_file()
        file_path = file.download()
        with open(file_path, 'rb') as f:
            send_to_eitaa("sendVoice", {}, {"voice": f})

    # فایل (سند مثل PDF, ZIP...)
    elif msg.document:
        file = msg.document.get_file()
        file_path = file.download()
        with open(file_path, 'rb') as f:
            send_to_eitaa("sendDocument", {"caption": msg.caption or ""}, {"document": f})

    else:
        print("ℹ️ نوع پیام پشتیبانی نشده:", msg)

# --- اجرای ربات تلگرام ---
updater = Updater(telegram_bot_token, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.chat(username=telegram_channel), forward_to_eitaa))

print("🚀 ربات آماده است و داره پیام‌ها رو از تلگرام به ایتا می‌فرسته...")
updater.start_polling()
updater.idle()
