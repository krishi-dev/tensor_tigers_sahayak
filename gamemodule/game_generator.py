# game_generator.py
import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

def remove_code_fences(text):
    lines = text.splitlines()
    cleaned_lines = []

    inside_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            inside_code_block = not inside_code_block
            continue
        if inside_code_block or stripped:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

load_dotenv('.env')

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

try:
    model = init_chat_model("gemini-2.5-pro", model_provider="google_genai")
except Exception as e:
    print(f"Failed to initialize the chat model: {e}")
    exit()
def  generate_game_code(context):
    prompt = f"""
You are a JavaScript game developer creating simple 2D educational games for children using **HTML5 Canvas** and **vanilla JavaScript** (no external libraries like Phaser.js or p5.js).

Generate a complete **HTML file** with embedded JavaScript that teaches the topic: **"{context}"** in a fun, interactive, and age-appropriate way for a 5th-grade student (around 10–11 years old).

Requirements:
1. The code must be a single, complete **HTML file**.
2. Include **Canvas-based visuals**, animations, and interactivity.
3. The game must be **educational** and reflect the topic "{context}" — e.g., clickable sorting items, correct/incorrect scoring, movement, or decision making.
4. Add clear instructions, simple score tracking, and gradually increasing difficulty (if possible).
5. Use bright colors, simple shapes, or sprite-like drawings with HTML5 Canvas only.
6. Return the code as plain text — no markdown or triple backticks.

Example Topics: Waste Management (separating items), Nutrition (classifying food), Energy Types (match renewable sources), etc.

Generate only the HTML code as plain text — no explanations.
"""
    try:
        s = model.invoke(prompt)
        return remove_code_fences(s.content)
    except Exception as e:
        print(f"An error occurred while invoking the model: {e}")
        return None

