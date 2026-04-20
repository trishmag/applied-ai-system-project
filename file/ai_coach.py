import os
from dotenv import load_dotenv
import google.generativeai as genai

# Explicitly load environment variables so the API key is always found
load_dotenv()

# Allow overriding the model via env so users can choose a model they have access to
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

def get_ai_hint(history: list, low: int, high: int, attempts: int) -> str:
    """
    Calls Gemini to analyze the player's guessing strategy and return a coaching tip.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Set GEMINI_API_KEY in your .env file to enable AI coaching."

    genai.configure(api_key=api_key)
    model_name = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
    try:
        model = genai.GenerativeModel(model_name)
    except Exception:
        # Let the generate_content call surface model-specific errors; we still continue
        model = genai.GenerativeModel(model_name)

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
        msg = str(e)
        # Provide an actionable message when the model isn't available for this key
        if "not found" in msg or "404" in msg or "is not found" in msg:
            return (
                f"⚠️ AI Coach unavailable: model '{model_name}' not found for this API key. "
                "If you have access to a different Gemini model, set GEMINI_MODEL in your .env (for example: GEMINI_MODEL=gemini-1.0) or use the provider's ListModels API to see available models."
            )
        if "unauthorized" in msg.lower() or "401" in msg:
            return "⚠️ AI Coach unavailable: API key appears invalid or unauthorized. Check your GEMINI_API_KEY."
        return f"⚠️ AI Coach unavailable: {msg}"


def get_glitch_analysis(history: list, outcomes: list, secret: int) -> str:
    """
    Calls Gemini to check whether the hint results look correct given the secret number.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Set GEMINI_API_KEY in your .env file to enable glitch analysis."

    genai.configure(api_key=api_key)
    model_name = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
    try:
        model = genai.GenerativeModel(model_name)
    except Exception:
        model = genai.GenerativeModel(model_name)

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
        msg = str(e)
        if "not found" in msg or "404" in msg or "is not found" in msg:
            return (
                f"⚠️ Glitch analysis unavailable: model '{model_name}' not found for this API key. "
                "Set GEMINI_MODEL in your .env to a model you can access, or call ListModels on the provider to see available models."
            )
        if "unauthorized" in msg.lower() or "401" in msg:
            return "⚠️ Glitch analysis unavailable: API key appears invalid or unauthorized. Check your GEMINI_API_KEY."
        return f"⚠️ Glitch analysis unavailable: {msg}"
