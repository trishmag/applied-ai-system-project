# evaluator.py
# Simulates many games automatically and reports reliability statistics.

import random
from logic_utils import get_range_for_difficulty, check_guess, update_score


def simulate_game(difficulty: str = "Normal", strategy: str = "binary") -> dict:
    """
    Simulates one complete game using either binary search or random guessing.
    Returns a dict with game outcome stats.
    """
    low, high = get_range_for_difficulty(difficulty)
    secret = random.randint(low, high)

    attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
    attempt_limit = attempt_limit_map.get(difficulty, 8)

    attempts = 0
    score = 0
    current_low = low
    current_high = high
    won = False

    while attempts < attempt_limit:
        if strategy == "binary":
            guess = (current_low + current_high) // 2
        else:
            guess = random.randint(current_low, current_high)

        attempts += 1
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempts)

        if outcome == "Win":
            won = True
            break
        elif outcome == "Too High":
            current_high = guess - 1
        else:
            current_low = guess + 1

    return {
        "won": won,
        "attempts": attempts,
        "score": score,
        "difficulty": difficulty,
        "strategy": strategy,
    }


def run_reliability_eval(n: int = 100, difficulty: str = "Normal") -> dict:
    """
    Runs n simulated games with binary search strategy and returns aggregate stats.
    """
    results = [simulate_game(difficulty, strategy="binary") for _ in range(n)]

    wins = sum(1 for r in results if r["won"])
    avg_attempts = sum(r["attempts"] for r in results) / n
    avg_score = sum(r["score"] for r in results) / n
    win_rate = round(wins / n * 100, 1)

    return {
        "total_games": n,
        "wins": wins,
        "losses": n - wins,
        "win_rate_pct": win_rate,
        "avg_attempts": round(avg_attempts, 2),
        "avg_score": round(avg_score, 2),
        "difficulty": difficulty,
    }


if __name__ == "__main__":
    for diff in ["Easy", "Normal", "Hard"]:
        stats = run_reliability_eval(n=200, difficulty=diff)
        print(f"\n--- {diff} ({stats['total_games']} games) ---")
        print(f"  Win rate:     {stats['win_rate_pct']}%")
        print(f"  Avg attempts: {stats['avg_attempts']}")
        print(f"  Avg score:    {stats['avg_score']}")
