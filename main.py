import os
import telebot
from google import genai
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
BOT_TOKEN = '8536803208:AAGrJzRPf1hoIApkaRHpkBAPhlbfQIJSt7k'
GEMINI_KEY = 'AIzaSyBuXuXH3JUxQnLBpoVdJr5GKsFORAe9udw'
CHANNEL_ID = "@Anokha_animation12" 
# Aapka YouTube Channel Link yahan hai
YT_LINK = "https://youtube.com/@anokhaanimation12?si=6K5-y6ua8REC_mZf"

# Initialize Clients
bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)
app = Flask('')

@app.route('/')
def home(): return "Bot is Active 🚀"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()

# Subscription Check Logic
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

# --- KEYBOARD SETUP ---
def get_verification_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    btn_yt = telebot.types.InlineKeyboardButton("📺 Subscribe YouTube", url=YT_LINK)
    btn_tg = telebot.types.InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/Anokha_animation12")
    markup.add(btn_yt)
    markup.add(btn_tg)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "✅ **Welcome!** Ab koi bhi topic bhejein, main viral SEO generate karunga.")
    else:
        bot.send_message(
            message.chat.id, 
            f"🚫 **Access Denied!**\n\nBot use karne ke liye hamara YouTube aur Telegram join karna zaroori hai.",
            reply_markup=get_verification_markup()
        )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not is_subscribed(message.from_user.id):
        bot.reply_to(message, "❌ Pehle dono channels join karein!", reply_markup=get_verification_markup())
        return

    sent_msg = bot.reply_to(message, "⏳ **Gemini AI is generating Pro SEO...**")
    try:
        # Gemini API Call
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"Generate viral YouTube SEO Title, Description, and Tags for: {message.text}"
        )
        
        bot.edit_message_text(f"🎯 **SEO Results:**\n\n{response.text}", 
                             chat_id=message.chat.id, message_id=sent_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Gemini Error: API Key check karein ya thodi der baad try karein.", message.chat.id, sent_msg.message_id)

if __name__ == "__main__":
    keep_alive()
    print("🚀 Bot is LIVE with YouTube Link!")
    bot.infinity_polling()
