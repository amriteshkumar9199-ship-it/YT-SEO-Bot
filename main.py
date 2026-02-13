import os
import telebot
import requests
import time
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
BOT_TOKEN = '8536803208:AAGrJzRPf1hoIApkaRHpkBAPhlbfQIJSt7k'
GEMINI_KEY = 'AIzaSyBuXuXH3JUxQnLBpoVdJr5GKsFORAe9udw'
CHANNEL_ID = "@Anokha_animation12" 
YT_SUB_LINK = "https://youtube.com/@anokhaanimation12?si=6K5-y6ua8REC_mZf"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Active 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- LOGIC: Subscription Check ---
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# --- UI: Keyboard ---
def get_start_keyboard():
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("📺 Subscribe YouTube", url=YT_SUB_LINK)
    btn2 = telebot.types.InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/{CHANNEL_ID.replace('@','')}")
    btn3 = telebot.types.InlineKeyboardButton("✅ I have Subscribed", callback_data="check_verif")
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "✅ **Access Granted!**\n\nAb aap topic bhejein, main SEO tags bana dunga.")
    else:
        bot.send_message(message.chat.id, "⚠️ **Verification Required!**", reply_markup=get_start_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "check_verif")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.edit_message_text("✅ **Success!** Ab topic bhejein.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ Pehle dono join karein!", show_alert=True)

# --- LOGIC: Gemini SEO (Fast & Robust) ---
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "🚫 Join channels first!", reply_markup=get_start_keyboard())
        return

    # Thumbnail Check
    if "youtube.com" in message.text or "youtu.be" in message.text:
        bot.reply_to(message, "📸 Extracting Thumbnail...")
        # (Thumbnail logic remains same)
        return

    # Gemini SEO Logic
    sent_msg = bot.reply_to(message, "⏳ **Gemini AI is generating SEO...**")
    
    # Fast Search Link
    search_link = f"https://www.youtube.com/results?search_query={message.text.replace(' ', '+')}"
    
    # API Request Logic
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Generate viral YouTube SEO Title, Description, and Tags for: {message.text}"}]
        }]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        
        # LOGIC: Check if Gemini returned content
        if 'candidates' in data and len(data['candidates']) > 0:
            seo_text = data['candidates'][0]['content']['parts'][0]['text']
            bot.edit_message_text(f"🎯 **SEO Results:**\n\n{seo_text}\n\n🔗 [Related Videos]({search_link})", 
                                 chat_id=message.chat.id, 
                                 message_id=sent_msg.message_id, 
                                 parse_mode='Markdown')
        else:
            bot.edit_message_text(f"⚠️ Gemini busy hai. Search link: {search_link}", message.chat.id, sent_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Error! Related videos: {search_link}", message.chat.id, sent_msg.message_id)

if __name__ == "__main__":
    keep_alive()
    print("🚀 Bot Started Successfully!")
    bot.infinity_polling()
