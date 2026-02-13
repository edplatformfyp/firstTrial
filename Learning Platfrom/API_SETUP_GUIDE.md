# API Key Setup Guide

To run EduCore for free, you need API keys from **Groq** (for fast text generation) and **Google Gemini** (as a backup/alternative). Both offer generous free tiers.

## Option 1: Groq API Key (Recommended for Speed)
1. Go to the [Groq Cloud Console](https://console.groq.com/keys).
2. **Log in** (you can use your Google/GitHub account).
3. Click on **"Create API Key"**.
4. Give it a name like "EduCore".
5. **Copy** the key starting with `gsk_...`.
6. Open your `.env` file in VS Code.
7. Paste it after `GROQ_API_KEY=`.

## Option 2: Google Gemini API Key (Reliable Free Tier)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. **Log in** with your Google account.
3. Click **"Create API key"**.
4. Select a project (or create a new one).
5. **Copy** the key.
6. Open your `.env` file in VS Code.
7. Paste it after `GEMINI_API_KEY=`.

## Final `.env` File
Your file at `d:\Desktop\Learning Platfrom\.env` should look like this (but with your actual random codes):

```env
GROQ_API_KEY=gsk_8A...
GEMINI_API_KEY=AIzaSy...
```

**Save the file** (Ctrl+S) after pasting.
