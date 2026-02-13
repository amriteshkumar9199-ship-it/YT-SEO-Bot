import os
import telebot
import requests
import time
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
BOT_TOKEN = '8536803208:AAGrJzRPf1hoIApkaRHpkBAPhlbfQIJSt7k'
GEMINI_KEY = 'AIzaSyDFPpGsEMhCfgdvzg7bR0Cc_5CTEelYUeA'
CHANNEL_ID = "@Anokha_animation12" 
YT_LINK = "https://youtube.com/@anokhaanimation12?si=6K5-y6ua8REC_mZf"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is 24/7 Active 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CHECK SUBSCRIPTION FUNCTION ---
def is_subscribed(user_id):
    try:
        # Iske liye bot ko Channel ka ADMIN banana zaroori hai
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# --- KEYBOARD FOR JOINING ---
def join_keyboard():
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("📺 Subscribe YouTube", url=YT_LINK)
    btn2 = telebot.types.InlineKeyboardButton("📢 Join Telegram Channel", url=f"https://t.me/{CHANNEL_ID.replace('@','')}")
    btn3 = telebot.types.InlineKeyboardButton("🔄 Click After Joining", callback_data="check_sub")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "✅ **Access Granted!**\n\nAb aap bot use kar sakte hain. Bas kisi topic ka naam bhejein.")
    else:
        bot.send_message(
            message.chat.id, 
            "⚠️ **Aapne hamara channel join nahi kiya hai!**\n\nBot use karne ke liye niche diye gaye buttons par click karke join karein aur 'Click After Joining' dabayein.",
            reply_markup=join_keyboard()
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Thank you! Ab bot chalu ho gaya hai.")
        bot.edit_message_text("✅ **Shukriya!**\n\nBot ab active hai. Topic likhein ya YouTube link bhejein.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ Aapne abhi join nahi kiya hai!", show_alert=True)

# --- Baki SEO aur Thumbnail ka logic pehle wala hi rahega ---
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "🚫 Pehle channel join karein!", reply_markup=join_keyboard())
        return
    
    # Yahan pehle wala SEO aur Thumbnail logic paste karein...
    bot.reply_to(message, "⚙️ Processing your request...")

if __name__ == "__main__":
    keep_alive()
    print("🚀 Bot with Verification Button is Running!")
    bot.infinity_polling()
