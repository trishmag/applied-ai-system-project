import os
from dotenv import load_dotenv
import google.generativeai as genai

# Explicitly load environment variables so the API key is always found
load_dotenv()

def get_ai_hint(history: list, low: int, high: int, attempts: int) -> str:
    """
    Calls Gemini to analyze the player's guessing strategy and return a coaching tip.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Set GEMINI_API_KEY in your .env file to enable AI coaching."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    history_str = ", ".join(str(g) for g in history) if history else "No guesses yet"

    prompt = f"""You are a friendly AI coach for a number guessing game.
The player is guessing a number between {low} and {high}.
They have made {attempts} guess(es) so far: {history_str}

Analyze their guessing strategy in 2-3 short sentences.
Check if they are using an efficient strategy like binary search (always guessing the midpoint).
Be encouraging and specific. Do not reveal the secret number. Keep it concise."""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ AI Coach unavailable: {str(e)}"


def get_glitch_analysis(history: list, outcomes: list, secret: int) -> str:
    """
    Calls Gemini to check whether the hint results look correct given the secret number.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Set GEMINI_API_KEY in your .env file to enable glitch analysis."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    pairs = "\n".join(
        f"  Guess: {g}, Hint given: {o}" for g, o in zip(history, outcomes)
    )

    prompt = f"""You are a game debugger reviewing a number guessing game for logic errors.
Secret number: {secret}

Here are the guess/hint pairs from this session:
{pairs}

For each pair, check: given the secret number, was the hint correct?
- If guess > secret, hint should be "Too High"
- If guess < secret, hint should be "Too Low"
- If guess == secret, hint should be "Win"

Give a 2-3 sentence verdict. Flag any incorrect hints as a glitch."""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ Glitch analysis unavailable: {str(e)}"
