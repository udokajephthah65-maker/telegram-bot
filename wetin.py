import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai

# --- FAKE WEB LAYER TO TRICK RENDER FREE TIER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot status: Active and operational."

def run_web_server():
    # Render automatically injects a "PORT" environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
# -----------------------------------------------

# Securely fetch tokens from Environment Variables
TELEGRAM_TOKEN = os.environ.get("8889180431:AAFSxQNwUdLuyZMu8x6l99UG96cmQ0axPY8")
GEMINI_API_KEY = os.environ.get("AIzaSyAGmvXNQaLRqRpoSDEWMHiQKgkQKDSIsdM")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("CRITICAL ERROR: Environment variables are missing!")

genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Base Personality Blueprint
SYSTEM_GUIDELINES = """
You are "AI Tutor," an elite educational assistant.
By default, provide thorough, deeply detailed, and well-explained answers.
If the user explicitly asks you to 'say a little', 'be brief', or 'keep it short', switch instantly to a short, direct answer.

Formatting Rules:
- DO NOT use code blocks (```) for regular text responses. 
- Use plain text line breaks and bullet points.
- End your responses with a short question to check understanding.
"""

AVAILABLE_MODELS = [
    "models/gemini-3.5-flash",
    "models/gemini-2.5-flash",
    "models/gemini-pro"
]

bot_memory = {}

def get_or_create_history(chat_id):
    if chat_id not in bot_memory:
        bot_memory[chat_id] = [
            {"role": "user", "parts": [f"System Framework: {SYSTEM_GUIDELINES}"]},
            {"role": "model", "parts": ["Understood."]}
        ]
    return bot_memory[chat_id]

def generate_with_memory(chat_id, new_message_text, visual_payload=None):
    history = get_or_create_history(chat_id)
    if visual_payload:
        user_content = [visual_payload, new_message_text]
    else:
        user_content = [new_message_text]
        
    history.append({"role": "user", "parts": user_content})
    
    for model_name in AVAILABLE_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(history)
            history.append({"role": "model", "parts": [response.text]})
            return response.text
        except Exception as e:
            continue
            
    history.pop()  
    raise Exception("All active models encountered connectivity boundaries.")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.chat.id in bot_memory:
        del bot_memory[message.chat.id]
    welcome_text = "Hello! I am an educational assistant bot created by Udoka Jephthah. How can I help you today?"
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio_query(message):
    try:
        bot.send_chat_action(message.chat.id, 'record_audio')
        file_id = message.voice.file_id if message.voice else message.audio.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        audio_part = {"mime_type": "audio/ogg;codecs=opus", "data": downloaded_file}
        instruction_string = "Task: Listen to this voice update and respond while remembering our previous chat conversation context."
        reply_text = generate_with_memory(message.chat.id, instruction_string, visual_payload=audio_part)
        bot.reply_to(message, reply_text)
    except Exception as e:
        bot.reply_to(message, f"Audio processing error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_academic_query(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        reply_text = generate_with_memory(message.chat.id, message.text)
        bot.reply_to(message, reply_text)
    except Exception as e:
        bot.reply_to(message, f"Text processing error: {e}")

if __name__ == "__main__":
    # 1. Start the web server in a side thread so Render stays happy
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # 2. Run your regular Telegram bot listening loop
    print("Educational Bot is live on Render Free Tier...")
    bot.delete_webhook(drop_pending_updates=True)
    bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
