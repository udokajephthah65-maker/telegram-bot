import os
import telebot
import google.generativeai as genai

# 1. Initialize tokens
TELEGRAM_TOKEN = "8889180431:AAFSxQNwUdLuyZMu8x6l99UG96cmQ0axPY8"
GEMINI_API_KEY = "AIzaSyAGmvXNQaLRqRpoSDEWMHiQKgkQKDSIsdM"

genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 2. Base Personality Blueprint
SYSTEM_GUIDELINES = """
You are "AI Tutor," an elite educational assistant.
By default, provide thorough, deeply detailed, and well-explained answers to help the user learn.
However, if the user explicitly asks you to 'say a little', 'be brief', or 'keep it short', switch instantly to an incredibly short, direct answer.

Formatting Rules:
- DO NOT use code blocks (```) for regular text responses. 
- Use plain text line breaks and bullet points to keep explanations readable.
- End your responses with a short question to check the student's understanding.
"""

AVAILABLE_MODELS = [
    "models/gemini-3.5-flash",
    "models/gemini-2.5-flash",
    "models/gemini-pro"
]

# 3. Memory Database Dictionary
# Key: chat_id | Value: List of past message objects
bot_memory = {}

def get_or_create_history(chat_id):
    """Ensures each unique user has an active memory thread initialized with system rules."""
    if chat_id not in bot_memory:
        bot_memory[chat_id] = [
            {"role": "user", "parts": [f"System Framework: {SYSTEM_GUIDELINES}"]},
            {"role": "model", "parts": ["Understood. I will provide comprehensive, well-explained tutorials, switching to short replies only when requested."]}
        ]
    return bot_memory[chat_id]

def generate_with_memory(chat_id, new_message_text, visual_payload=None):
    """Appends new messages to user history, processes through models, and updates memory."""
    history = get_or_create_history(chat_id)
    
    # Pack the user input layout correctly
    if visual_payload:
        # For audio inputs, we inject the message string alongside file bytes
        user_content = [visual_payload, new_message_text]
    else:
        user_content = [new_message_text]
        
    # Append current input to memory stack
    history.append({"role": "user", "parts": user_content})
    
    # Try models cascading down the list
    for model_name in AVAILABLE_MODELS:
        try:
            print(f"Routing conversation to: {model_name}...")
            model = genai.GenerativeModel(model_name)
            
            # Sending the full historical chat array instead of just a single line
            response = model.generate_content(history)
            
            # Save the bot's reply text to its memory bank
            history.append({"role": "model", "parts": [response.text]})
            return response.text
            
        except Exception as e:
            print(f"Notice: Model {model_name} bypassed. Reason: {e}")
            continue
            
    # Clean rollback if everything errors out
    history.pop()  # Remove last entry to prevent corruption
    raise Exception("All active models encountered connectivity boundaries.")


print("Educational Bot is live with Long-Term Chat Memory enabled...")

# Handle /start or /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Wipe memory clear on a fresh start command
    if message.chat.id in bot_memory:
        del bot_memory[message.chat.id]
        
    welcome_text = "Hello! I am an educational assistant bot created by Udoka Jephthah. I can now remember our full chat history! How can I help you today?"
    bot.reply_to(message, welcome_text)


# Handle incoming Audio and Voice Notes
@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio_query(message):
    try:
        bot.send_chat_action(message.chat.id, 'record_audio')
        
        file_id = message.voice.file_id if message.voice else message.audio.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        
        audio_part = {
            "mime_type": "audio/ogg;codecs=opus",
            "data": downloaded_file
        }
        
        instruction_string = "Task: Listen to this voice update and respond while remembering our previous chat conversation context."
        
        reply_text = generate_with_memory(message.chat.id, instruction_string, visual_payload=audio_part)
        bot.reply_to(message, reply_text)
        
    except Exception as e:
        print(f"CRITICAL AUDIO ERROR LOG: {e}")
        bot.reply_to(message, f"Audio processing error: {e}")


# Handle all incoming text messages
@bot.message_handler(func=lambda message: True)
def handle_academic_query(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Route directly through memory matrix
        reply_text = generate_with_memory(message.chat.id, message.text)
        bot.reply_to(message, reply_text)
        
    except Exception as e:
        print(f"CRITICAL TEXT ERROR LOG: {e}")
        bot.reply_to(message, f"Text processing error: {e}")

# Clean hooks and activate polling loops
bot.delete_webhook(drop_pending_updates=True)
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
