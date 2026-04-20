# logic_utils.py

def get_range_for_difficulty(difficulty: str) -> tuple:
    """Returns the (low, high) range for the chosen difficulty."""
    if difficulty == "Easy":
        return 1, 20
    elif difficulty == "Hard":
        return 1, 50
    else:  # Normal or unknown
        return 1, 100

def parse_guess(raw_guess) -> tuple:
    """Validates the input string and returns (is_valid, value, error_message)."""
    if raw_guess is None or raw_guess == "":
        return False, None, "Please enter a number."
    
    try:
        val = int(float(raw_guess)) # Handles both "7" and "7.9"
        return True, val, None
    except ValueError:
        return False, None, "Please enter a valid integer."

def check_guess(guess: int, secret: int) -> tuple:
    """Compares guess to secret and returns (outcome, message)."""
    if guess == secret:
        return "Win", "Correct! You guessed it."
    elif guess > secret:
        return "Too High", "Too high! Try again."
    else:
        return "Too Low", "Too low! Try again."

def update_score(score: int, outcome: str, attempts: int) -> int:
    """Updates the score based on game outcome."""
    if outcome == "Win":
        # Based on test_game_logic.py: 100 - (10 * attempts)
        new_score = 100 - (10 * attempts)
        return max(new_score, 10) # Ensure score doesn't drop below 10 on win
    elif outcome in ["Too High", "Too Low"]:
        return score - 5
    return score