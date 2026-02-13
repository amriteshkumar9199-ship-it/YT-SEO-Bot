import os
import telebot
from google import genai
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
BOT_TOKEN = '8536803208:AAGrJzRPf1hoIApkaRHpkBAPhlbfQIJSt7k'
GEMINI_KEY = 'AIzaSyBuXuXH3JUxQnLBpoVdJr5GKsFORAe9udw'
CHANNEL_ID = "@Anokha_animation12" 
YT_SUB_LINK = "https://youtube.com/@anokhaanimation12?si=6K5-y6ua8REC_mZf"

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

# Subscription Check
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "✅ **Access Granted!** Topic bhejein SEO ke liye.")
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📺 Subscribe YouTube", url=YT_SUB_LINK))
        markup.add(telebot.types.InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/Anokha_animation12"))
        bot.send_message(message.chat.id, "🚫 Pehle Subscribe aur Join karein!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not is_subscribed(message.from_user.id):
        bot.reply_to(message, "❌ Pehle channel join karein!")
        return

    # SEO Logic using New SDK from your photo
    sent_msg = bot.reply_to(message, "⏳ **Gemini AI is generating SEO...**")
    try:
        # Using the model from your image: gemini-2.0-flash (fastest)
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"Generate viral YouTube SEO Title, Description, and Tags for: {message.text}"
        )
        
        seo_text = response.text
        search_link = f"https://www.youtube.com/results?search_query={message.text.replace(' ', '+')}"
        
        bot.edit_message_text(f"🎯 **SEO Results:**\n\n{seo_text}\n\n🔗 [Related Videos]({search_link})", 
                             chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode='Markdown')
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, sent_msg.message_id)

if __name__ == "__main__":
    keep_alive()
    print("🚀 Bot Started with New Gemini SDK!")
    bot.infinity_polling()
