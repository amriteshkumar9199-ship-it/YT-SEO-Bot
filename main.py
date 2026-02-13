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
# Aapka YouTube Channel Link
YT_CHANNEL_URL = "https://youtube.com/@anokhaanimation12?si=6K5-y6ua8REC_mZf"

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

# --- VERIFICATION LOGIC ---
def is_subscribed(user_id):
    try:
        # Bot ko Channel ka Admin banana zaroori hai
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "✅ **Welcome!**\n\n1. **SEO:** Kisi topic ka naam bhejein.\n2. **Thumbnail:** YouTube link bhejein.")
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton("📺 Subscribe YouTube", url=YT_CHANNEL_URL)
        btn2 = telebot.types.InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/{CHANNEL_ID.replace('@','')}")
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.chat.id, "🚫 **Access Denied!**\n\nBot use karne ke liye YouTube aur Telegram join karna zaroori hai. Join karke phir se /start dabayein.", reply_markup=markup)

# --- SEO, THUMBNAIL & SEARCH LOGIC ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not is_subscribed(message.from_user.id):
        bot.reply_to(message, "❌ Pehle channel join karein!")
        return

    # 1. Thumbnail Extraction
    if "youtube.com" in message.text or "youtu.be" in message.text:
        try:
            v_id = message.text.split("v=")[1].split("&")[0] if "v=" in message.text else message.text.split("/")[-1].split("?")[0]
            thumb_url = f"https://img.youtube.com/vi/{v_id}/maxresdefault.jpg"
            bot.send_photo(message.chat.id, thumb_url, caption="✅ Aapka HD Thumbnail taiyaar hai!")
        except:
            bot.reply_to(message, "❌ Invalid YouTube Link")
        return

    # 2. SEO Generation & Search Link
    bot.send_message(message.chat.id, "⏳ Generating SEO Results... Please wait.")
    
    # YouTube Search Link Creation
    search_query = message.text.replace(" ", "+")
    yt_search_url = f"https://www.youtube.com/results?search_query={search_query}"
    
    # Gemini API Call
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Write viral YouTube SEO tags, description and 3 titles for: {message.text}"}]}]}
    
    try:
        r = requests.post(url, json=payload)
        data = r.json()
        content = data['candidates'][0]['content']['parts'][0]['text']
        
        final_msg = (
            f"🎯 **SEO for:** {message.text}\n\n"
            f"{content}\n\n"
            f"🔗 **Related Videos:** [Yahan Click Karein]({yt_search_url})"
        )
        bot.reply_to(message, final_msg, parse_mode='Markdown')
    except:
        bot.reply_to(message, f"⚠️ SEO generate nahi ho saka. Aap related videos yahan dekh sakte hain:\n{yt_search_url}")

if __name__ == "__main__":
    keep_alive()
    print("🚀 Bot is LIVE with YouTube Support!")
    bot.infinity_polling()
