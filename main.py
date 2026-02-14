import os, telebot, requests, time
from flask import Flask
from threading import Thread

# --- 1. CONFIGURATION ---
BOT_TOKEN = os.environ.get('BOT_TOKEN') # Koyeb Settings se uthayega
GEMINI_KEY = os.environ.get('GEMINI_KEY') # Koyeb Settings se uthayega

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home(): return "SEO Expert Bot is 24/7 Active 🚀"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run, daemon=True).start()

# --- 2. ADVANCED SEO LOGIC ---
def get_seo_expert_data(topic):
    # Direct API Call for speed
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    prompt = (
        f"You are a YouTube Viral Growth Expert. For the topic '{topic}', provide:\n"
        "1. 🚀 3 Viral Titles (High CTR)\n"
        "2. 📈 Top 20 Search Keywords (Tags for tags section)\n"
        "3. 📝 Professional SEO Description (with hashtags)\n"
        "4. 🖼️ Detailed Thumbnail Design Idea (Color, Text, Image suggestion)\n"
        "Make the output clean and easy to copy-paste."
    )
    
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
        res = r.json()
        return res['candidates'][0]['content']['parts'][0]['text']
    except:
        return "❌ Error: Gemini API Key check karein Koyeb settings mein."

# --- 3. BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(m):
    bot.reply_to(m, "👋 Welcome! Topic bhejein aur main viral SEO ideas generate kar dunga!")

@bot.message_handler(func=lambda m: True)
def handle_seo(m):
    status_msg = bot.reply_to(m, "⏳ **SEO is working... Please wait.**")
    bot.send_chat_action(m.chat.id, 'typing')
    
    final_seo = get_seo_expert_data(m.text)
    bot.edit_message_text(final_seo, m.chat.id, status_msg.message_id)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
