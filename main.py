from fastapi import FastAPI
from typing import Optional
import random

app = FastAPI()

# Expanded data: motivational quotes with multiple quotes per theme
quotes = [
    {"quote": "The best time to plant a tree was 20 years ago. The second best time is now.", "theme": "inspiration"},
    {"quote": "It’s not whether you get knocked down. It’s whether you get up.", "theme": "inspiration"},
    {"quote": "Your limitation—it's only your imagination.", "theme": "motivation"},
    {"quote": "Push yourself, because no one else is going to do it for you.", "theme": "motivation"},
    {"quote": "Sometimes later becomes never. Do it now.", "theme": "motivation"},
    {"quote": "Great things never come from comfort zones.", "theme": "adventure"},
    {"quote": "Dream it. Wish it. Do it.", "theme": "dreams"},
    {"quote": "Success doesn’t just find you. You have to go out and get it.", "theme": "success"},
    {"quote": "The harder you work for something, the greater you’ll feel when you achieve it.", "theme": "success"},
    {"quote": "Dream bigger. Do bigger.", "theme": "ambition"},
    {"quote": "Don’t stop when you’re tired. Stop when you’re done.", "theme": "perseverance"},
    {"quote": "Wake up with determination. Go to bed with satisfaction.", "theme": "determination"},
    {"quote": "Do something today that your future self will thank you for.", "theme": "futurism"},
    {"quote": "Little things make big days.", "theme": "positivity"},
    {"quote": "It’s going to be hard, but hard does not mean impossible.", "theme": "positivity"},
    {"quote": "Don’t wait for opportunity. Create it.", "theme": "opportunity"},
    {"quote": "Sometimes we’re tested not to show our weaknesses, but to discover our strengths.", "theme": "self-discovery"},
    {"quote": "The key to success is to focus on goals, not obstacles.", "theme": "focus"},
    {"quote": "Dream it. Believe it. Build it.", "theme": "creation"},
    {"quote": "Motivation is what gets you started. Habit is what keeps you going.", "theme": "habit"},
    {"quote": "All progress takes place outside the comfort zone.", "theme": "growth"},
    {"quote": "You don’t have to be great to start, but you have to start to be great.", "theme": "beginnings"},
]

emojis = {
    "inspiration": "🌟",
    "motivation": "💪",
    "adventure": "🚀",
    "dreams": "🌈",
    "success": "🏆",
    "ambition": "🔝",
    "perseverance": "🐘",
    "determination": "🔥",
    "futurism": "🌐",
    "positivity": "😊",
    "opportunity": "🚪",
    "self-discovery": "🔍",
    "focus": "🎯",
    "creation": "🛠️",
    "habit": "🔄",
    "growth": "📈",
    "beginnings": "🌱",
}

@app.get("/home/")
async def root():
    return {"message": "Welcome to the Motivational Quotes API! --- Version 1!"}

    # return {"message": "Welcome to the Motivational Quotes API! --- Version 2!"}


@app.get("/quote/")
async def get_quote(theme: Optional[str] = None):
    if theme:
        filtered_quotes = [quote for quote in quotes if quote["theme"] == theme]
        if not filtered_quotes:
            return {"message": "No quotes found for the specified theme."}
    else:
        filtered_quotes = quotes

    selected_quote = random.choice(filtered_quotes)
    quote_emoji = emojis[selected_quote["theme"]]
    return {"quote": selected_quote["quote"], "emoji": quote_emoji}

@app.get("/themes/")
async def get_themes():
    return {"themes": list(emojis.keys())}