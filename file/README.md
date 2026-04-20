# 🎮 Game Glitch Investigator — Applied AI System

## 📌 Base Project

This project extends **Game Glitch Investigator: The Impossible Guesser** (Module 1).
The original was a deliberately broken Streamlit number guessing game where students had to find and fix two bugs: a resetting secret number caused by Streamlit's rerun behavior, and reversed Higher/Lower hints. Core game logic was refactored into `logic_utils.py` with pytest coverage.

---

## 🚀 What This Extended System Does

This version extends the original game into a full applied AI system with three new capabilities:

1. **AI Strategy Coach** — Claude analyzes your guess history in real time and gives personalized strategic feedback (e.g., "Try binary search — always guess the midpoint!").
2. **AI Glitch Detector** — Claude reviews your hint history against the secret number and flags any logic errors, simulating an AI debugging assistant.
3. **Reliability Evaluator** — Runs hundreds of automated games using a binary search agent and reports win rate, average attempts, and average score by difficulty.

All events are logged to `game_log.txt` for audit and debugging purposes.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit UI (app.py)              │
│   ┌──────────┐   ┌──────────────┐   ┌────────────┐  │
│   │ 🎮 Game  │   │ 🤖 AI Coach  │   │ 📊 Eval    │  │
│   └────┬─────┘   └──────┬───────┘   └─────┬──────┘  │
└────────┼────────────────┼─────────────────┼──────────┘
         │                │                 │
         ▼                ▼                 ▼
  logic_utils.py     ai_coach.py       evaluator.py
  (game rules)     (Claude API calls)  (sim engine)
         │                │                 │
         ▼                ▼                 │
   session_state    Anthropic API           │
   (Streamlit)      claude-sonnet           │
         │                                  │
         └──────────────────────────────────┘
                          │
                          ▼
                     logger.py
                   game_log.txt
```

**Data flow:** User input → Streamlit UI → game logic validates and updates state → AI coach optionally called with guess history → Claude returns coaching tip → evaluator runs simulated games independently → all events logged.

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/trishmag/applied-ai-system-project.git
cd applied-ai-system-project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY=your_key_here
```
> The game runs without this key — AI Coach and Glitch Detector will show a warning instead of crashing.

### 4. Run the app
```bash
python -m streamlit run app.py
```

### 5. Run tests
```bash
pytest test_game_logic.py -v
```

---

## 💬 Sample Interactions

### Example 1 — AI Coach tip after poor guesses
**Input:** Player guesses 10, 90, 45 (on Normal difficulty, secret = 62)
**AI Coach output:**
> "Your guesses are jumping around quite a bit! After getting 'Too Low' on 45, the number must be between 46 and 90. Try guessing 68 next — that's the midpoint of your remaining range and narrows it down fastest."

### Example 2 — Glitch Detector on correct logic
**Input:** Guesses 50 (Too Low), 75 (Too High), 62 (Win), secret = 62
**AI output:**
> "All hints look correct. A guess of 50 against secret 62 correctly returned Too Low, 75 correctly returned Too High, and 62 correctly returned Win. No glitches detected in this session."

### Example 3 — Reliability Evaluator on Hard difficulty
**Input:** 200 simulated games, Hard difficulty (range 1–50, 5 attempts)
**Output:**
```
Win Rate:    95.5%
Avg Attempts: 4.8
Avg Score:   45.2
```

---

## 🎨 Design Decisions

- **Claude as coach, not judge:** The AI never reveals the secret number — it only advises on strategy. This preserves game integrity.
- **Graceful degradation:** If `ANTHROPIC_API_KEY` is missing, the game still fully works. AI features show a clear warning rather than crashing.
- **Separation of concerns:** `logic_utils.py` stays pure Python with no AI dependencies, keeping tests fast and deterministic.
- **Binary search agent in evaluator:** Using binary search (not random) gives a meaningful upper-bound benchmark for how well the game logic performs under optimal play.
- **Logging over print statements:** All events write to `game_log.txt` so issues can be reproduced after the fact.

---

## 🧪 Testing Summary

**17 pytest tests** covering `check_guess`, `parse_guess`, `update_score`, `get_range_for_difficulty`, `simulate_game`, and `run_reliability_eval`.

Key findings:
- All 17 tests pass after fixes ✅
- Binary search wins 100% of Easy games (confirmed mathematically: ceil(log₂(20)) = 5 guesses, limit is 6)
- Reliability eval confirms Hard difficulty has ~5% loss rate even with optimal play, which is expected (range 1–50, 5 attempts)
- `parse_guess` correctly handles None, empty string, floats, and letters

---

## 🔁 Loom Walkthrough

> [Insert your Loom link here after recording]

---

## 📁 File Structure

```
applied-ai-system-project/
├── app.py               # Streamlit UI with 3 tabs
├── logic_utils.py       # Core game logic (pure Python)
├── ai_coach.py          # Claude-powered coaching and glitch detection
├── evaluator.py         # Automated reliability simulation
├── logger.py            # File-based event logger
├── test_game_logic.py   # Expanded pytest suite (17 tests)
├── requirements.txt     # Dependencies
├── README.md            # This file
├── model_card.md        # Reflection and AI collaboration notes
├── game_log.txt         # Auto-generated event log (gitignored)
└── assets/
    └── architecture.png # System diagram screenshot
```
