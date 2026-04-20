# test_game_logic.py
# Expanded test suite covering logic_utils and evaluator.

import pytest
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty
from evaluator import simulate_game, run_reliability_eval


# ─── check_guess ────────────────────────────────────────────
class TestCheckGuess:
    def test_winning_guess(self):
        outcome, _ = check_guess(50, 50)
        assert outcome == "Win"

    def test_guess_too_high(self):
        outcome, _ = check_guess(60, 50)
        assert outcome == "Too High"

    def test_guess_too_low(self):
        outcome, _ = check_guess(40, 50)
        assert outcome == "Too Low"

    def test_boundary_low(self):
        outcome, _ = check_guess(1, 1)
        assert outcome == "Win"

    def test_boundary_high(self):
        outcome, _ = check_guess(100, 100)
        assert outcome == "Win"

    def test_message_returned_on_win(self):
        _, msg = check_guess(50, 50)
        assert isinstance(msg, str) and len(msg) > 0

    def test_message_returned_on_high(self):
        _, msg = check_guess(80, 50)
        assert isinstance(msg, str) and len(msg) > 0


# ─── parse_guess ─────────────────────────────────────────────
class TestParseGuess:
    def test_valid_integer(self):
        ok, val, err = parse_guess("42")
        assert ok is True
        assert val == 42
        assert err is None

    def test_valid_float_rounds(self):
        ok, val, err = parse_guess("7.9")
        assert ok is True
        assert val == 7

    def test_empty_string(self):
        ok, _, err = parse_guess("")
        assert ok is False
        assert err is not None

    def test_none_input(self):
        ok, _, err = parse_guess(None)
        assert ok is False

    def test_letters(self):
        ok, _, err = parse_guess("abc")
        assert ok is False
        assert err is not None


# ─── update_score ────────────────────────────────────────────
class TestUpdateScore:
    def test_win_first_attempt(self):
        score = update_score(0, "Win", 1)
        assert score == 90  # 100 - 10*1

    def test_win_adds_minimum_10(self):
        # At attempt 10, max(100 - 100, 10) = 10
        score = update_score(0, "Win", 10)
        assert score == 10

    def test_too_high_deducts(self):
        score = update_score(50, "Too High", 1)
        assert score == 45

    def test_too_low_deducts(self):
        score = update_score(50, "Too Low", 1)
        assert score == 45

    def test_unknown_outcome_unchanged(self):
        score = update_score(50, "Unknown", 1)
        assert score == 50


# ─── get_range_for_difficulty ────────────────────────────────
class TestDifficultyRange:
    def test_easy(self):
        low, high = get_range_for_difficulty("Easy")
        assert low == 1 and high == 20

    def test_normal(self):
        low, high = get_range_for_difficulty("Normal")
        assert low == 1 and high == 100

    def test_hard(self):
        low, high = get_range_for_difficulty("Hard")
        assert low == 1 and high == 50

    def test_unknown_defaults_to_normal(self):
        low, high = get_range_for_difficulty("Unknown")
        assert low == 1 and high == 100


# ─── evaluator ───────────────────────────────────────────────
class TestEvaluator:
    def test_simulate_game_returns_dict(self):
        result = simulate_game("Normal", "binary")
        assert "won" in result
        assert "attempts" in result
        assert "score" in result

    def test_binary_always_wins_easy(self):
        # Binary search on Easy (1-20, 6 attempts) should always win
        # ceil(log2(20)) = 5 guesses needed at most
        for _ in range(20):
            result = simulate_game("Easy", "binary")
            assert result["won"] is True

    def test_reliability_eval_returns_stats(self):
        stats = run_reliability_eval(n=20, difficulty="Easy")
        assert stats["total_games"] == 20
        assert 0 <= stats["win_rate_pct"] <= 100
        assert stats["wins"] + stats["losses"] == stats["total_games"]
