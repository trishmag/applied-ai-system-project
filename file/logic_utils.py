# logic_utils.py

def get_range_for_difficulty(difficulty: str) -> tuple:
    if difficulty == "Easy":
        return 1, 20
    elif difficulty == "Hard":
        return 1, 50
    else:
        return 1, 100

# This MUST have 3 arguments to match your app.py call
def parse_guess(raw_guess, low=1, high=100) -> tuple:
    """Validates input string, converts to int, and checks range bounds.

    Notes:
    - Backwards compatible: callers may pass (raw_guess) or (raw_guess, low, high).
    - Defaults correspond to the 'Normal' difficulty range (1..100).
    """
    if raw_guess is None or raw_guess == "":
        return False, None, "Please enter a number."
    try:
        val = int(float(raw_guess))
        if val < low or val > high:
            return False, None, f"Please guess between {low} and {high}."
        return True, val, None
    except ValueError:
        return False, None, "Please enter a valid integer."

def check_guess(guess: int, secret: int) -> tuple:
    if guess == secret:
        return "Win", "Correct! You guessed it."
    elif guess > secret:
        return "Too High", "Too high! Try again."
    else:
        return "Too Low", "Too low! Try again."

def update_score(score: int, outcome: str, attempts: int) -> int:
    if outcome == "Win":
        return max(100 - (10 * attempts), 10)
    elif outcome in ["Too High", "Too Low"]:
        return score - 5
    return score
