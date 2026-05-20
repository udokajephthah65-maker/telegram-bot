# AI Tutor - Telegram Educational Bot 🚀

Welcome to the **AI Tutor** repository! This project is a mobile-deployed, resilient Telegram bot designed to serve as an elite, universally knowledgeable academic assistant. Built completely using Python and running on mobile environments via Pydroid 3, this bot assists students across various subjects (Physics, Mathematics, History, Literature, Coding, etc.) by providing deep, contextual, and well-explained answers.

---

## 📖 Project Overview & Intent

The primary goal of **AI Tutor** is to make personalized academic help accessible directly from a chat interface. Unlike basic Q&A bots, this system is engineered to behave like a human teacher:
* **Thorough Explanations:** It breaks down complex topics into digestible plain text segments with simple formatting.
* **Dynamic Response Control:** It dynamically adjusts its output length. By default, it thoroughly explains subjects, but if a user specifies to *"just say a little"* or *"be brief"*, it cuts directly to the core answer.
* **Multimodal Learning:** It processes both standard text queries and native voice notes/audio files.

---

## 🛠️ How the Code Was Engineered

This bot was developed over several developmental phases to overcome constraints typical of free-tier API endpoints and mobile execution environments. Below is a breakdown of how the architecture was built:

### 1. Unified Multi-Model Backup Pipeline (Fallback Engine)
To prevent the bot from crashing when hitting strict API rate limits or trial quotas (such as the 20-request limit on newer experimental models), the system implements a cascading fallback array. 

The script sequentially routes incoming requests down an active tier list of verified Google Generative AI endpoints:
1.  **`gemini-3.5-flash`** (Primary high-speed brain)
2.  **`gemini-2.5-flash`** (Secondary stable workhorse)
3.  **`gemini-pro`** (Tertiary permanent backup)

If the primary model returns a `429 Quota Exceeded` exception, the script catches the error, skips to the next active model in less than a second, and fulfills the request seamlessly without disrupting the Telegram user.

### 2. Conversational Memory Matrix
Standard API calls to large language models are stateless (they forget past interactions instantly). To fix this, a session-specific dictionary memory bank (`bot_memory`) was engineered. 
* Every user interaction (`chat_id`) initializes a unique thread containing the global pedagogical rules.
* The system continually appends user inputs and model outputs into a structured history matrix, allowing the bot to keep continuous context over complex, multi-step academic problem solving.

### 3. Safe Telegram Rendering (Anti-Code Formatting)
By default, advanced frontier models format educational explanations or programming tasks inside complex markdown formatting blocks (e.g., ` ``` `). Because raw markdown strings can easily crash standard Telegram wrapper connections if specific characters are unescaped, the system instruction pipeline strictly forces the model to respond in highly structured plain text using simple line breaks and standard bullet points.

---

## ✨ Features

* **Contextual Chat Memory:** Remembers past messages in a conversation thread so you can ask follow-up questions naturally.
* **Voice/Audio Comprehension:** Accepts audio messages (`.ogg` via Opus) and processes them directly through multimodal layers to interpret spoken educational questions.
* **Intelligent Fluff Filter:** Automatically eliminates boilerplate phrases (e.g., *"Sure, I can help you with that!"*) when short responses are requested.
* **Mobile-Ready & Lean:** Fully optimized to run seamlessly inside mobile IDE architectures like Pydroid 3 without heavy dependency overhead.

---

## 🗂️ Core Technology Stack

* **Programming Language:** Python 3
* **Telegram Framework:** `pyTelegramBotAPI` (`telebot`) - Used for handling webhook updates, chat actions (typing indicators), and incoming multimodal content types.
* **AI Engine:** `google-generativeai` - Google's official API library used to interface with the Gemini Flash and Pro model clusters.

---

## 🚀 Getting Started & Installation

To run this bot locally on your machine or inside **Pydroid 3** on an Android device, follow these steps:

### 1. Prerequisites
Ensure you have Python installed, then install the required dependencies using `pip`:
```bash
pip install pyTelegramBotAPI google-generativeai

```
### 2. Acquire API Access Tokens
 1. Create a bot on Telegram via @BotFather and copy your **Telegram Bot Token**.
 2. Go to Google AI Studio and generate your **Gemini API Key**.
### 3. Configuration
Open the script and replace the placeholder configuration values with your unique tokens at the top of the file:
```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

```
### 4. Running the Script
Execute the script from your terminal or hit the **Play** button inside Pydroid 3:
```bash
python bot.py

```
## 👨‍💻 Author
Created and engineered by **Udoka Jephthah** as an advanced, resilient educational tool.
```

---

### How to use this on GitHub:
1. Go to your GitHub repository named `G4-respiratory` (or your chosen repo name).
2. Click on **Add file** -> **Create new file**.
3. Name the file exactly **`README.md`**.
4. Paste the text block above right into the editor window.
5. Scroll down and click **Commit changes** to save it!

```
