from telethon import TelegramClient, events
import requests
import os
import logging
import time

# --- تنظیمات ---
api_id = 123456      # از my.telegram.org
api_hash = "YOUR_API_HASH"
telegram_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
telegram_channel = "telegram_channel_username"  # بدون @

eitaa_token = "YOUR_EITAA_BOT_TOKEN"
eitaa_channel = "@your_eitaa_channel"

# --- لاگ‌گذاری ---
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- کلاینت تلگرام ---
client = TelegramClient('forwarder', api_id, api_hash).start(bot_token=telegram_bot_token)

# --- ارسال متن به ایتا ---
def send_text_to_eitaa(text):
    url = f"https://eitaayar.ir/api/{eitaa_token}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": eitaa_channel, "text": text}, timeout=20)
        if r.status_code == 200:
            logging.info("✅ متن ارسال شد.")
        else:
            logging.error(f"خطا در ارسال متن: {r.text}")
    except Exception as e:
        logging.error(f"❌ خطا در اتصال به ایتا: {e}")

# --- ارسال فایل (عکس/ویدیو/ویس/سند) به ایتا ---
def send_file_to_eitaa(file_path, file_type):
    try:
        # بررسی سایز (محدودیت 50MB فرضی)
        if os.path.getsize(file_path) > 50 * 1024 * 1024:
            logging.warning(f"⚠️ فایل {file_path} خیلی بزرگه، ارسال نشد.")
            return

        url = f"https://eitaayar.ir/api/{eitaa_token}/send{file_type.capitalize()}"
        with open(file_path, 'rb') as f:
            r = requests.post(url, data={"chat_id": eitaa_channel}, files={file_type: f}, timeout=60)

        if r.status_code == 200:
            logging.info(f"✅ {file_type} ارسال شد.")
        else:
            logging.error(f"خطا در ارسال {file_type}: {r.text}")

    except Exception as e:
        logging.error(f"❌ خطا در ارسال فایل: {e}")
    finally:
        try:
            os.remove(file_path)  # پاکسازی
        except:
            pass

# --- وقتی پست جدید در تلگرام بیاد ---
@client.on(events.NewMessage(chats=telegram_channel))
async def handler(event):
    try:
        message = event.message

        if message.text:  
            send_text_to_eitaa(message.text)

        elif message.photo:  
            file_path = await message.download_media()
            send_file_to_eitaa(file_path, "photo")

        elif message.video:  
            file_path = await message.download_media()
            send_file_to_eitaa(file_path, "video")

        elif message.voice:  
            file_path = await message.download_media()
            send_file_to_eitaa(file_path, "voice")

        elif message.document:  
            file_path = await message.download_media()
            send_file_to_eitaa(file_path, "document")

        else:
            logging.info(f"پیام پشتیبانی نشده: {message.id}")

    except Exception as e:
        logging.error(f"❌ خطای ناشناخته در handler: {e}")
        time.sleep(5)  # جلوگیری از اسپم شدن خطا

print("🚀 ربات روشن است...")
client.run_until_disconnected()
