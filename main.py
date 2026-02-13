import os, telebot, requests, time
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get('BOT_TOKEN') #
GEMINI_KEY = os.environ.get('GEMINI_KEY') #
CHANNEL_ID = "@Anokha_animation12"
YT_LINK = "https://youtube.com/@anokhaanimation12?si=6K5-y6ua8REC_mZf" # Aapka YouTube Link

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home(): return "Bot is 24/7 Active 🚀"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run, daemon=True).start()

# --- FAST AI LOGIC ---
def get_ai_response(user_text):
    # Direct API call for maximum speed and No 404 Error
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    # AI ko instruction diya hai Tags, Description aur Thumbnail ideas ke liye
    prompt = f"Act as a YouTube SEO Expert. For the topic '{user_text}', provide: 1. Viral Title, 2. High Ranking Tags, 3. Short Description, 4. Eye-catching Thumbnail Idea. Keep it professional and fast."
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ API Error. Please check your Gemini Key in Koyeb Settings."

# --- HANDLERS ---
@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.send_chat_action(m.chat.id, 'typing')
    
    # AI se response lena
    ai_reply = get_ai_response(m.text)
    
    # YouTube Link Button wapas joda gaya hai
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔴 Subscribe YouTube", url=YT_LINK))
    
    bot.reply_to(m, ai_reply, reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    print("🚀 Anokha Animation Bot is LIVE on Koyeb!")
    bot.infinity_polling()
