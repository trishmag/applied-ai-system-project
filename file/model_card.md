# 🃏 Model Card — Game Glitch Investigator: Applied AI System

## 📌 Project Identity

**Project name:** Game Glitch Investigator — Applied AI System
**Base project:** Game Glitch Investigator: The Impossible Guesser (Module 1)
**Author:** Trish Mag
**Model used:** Claude (claude-sonnet-4-20250514) via Anthropic API

---

## 🤖 AI Feature: Agentic Coaching + Glitch Detection

The AI feature in this system is a **dual-purpose Claude agent** embedded in the Streamlit app. It serves two roles:

1. **Strategy Coach** — receives the player's guess history and range, then generates a 2-3 sentence coaching tip encouraging efficient binary search play.
2. **Glitch Detector** — receives guess/outcome pairs alongside the secret number and determines whether the hints were logically correct. This simulates an AI that can audit its own game for bugs.

The agent is invoked on demand (not automatically), and its output directly changes what the user sees — making it a meaningful part of the system rather than a decoration.

---

## ⚠️ Limitations and Biases

- **No memory across sessions:** Claude receives only the current session's history. It cannot compare this game to previous games or learn from patterns across players.
- **Trusts the data it receives:** The glitch detector relies on the secret number being passed correctly. If the app had a bug that corrupted session state, Claude would analyze the wrong data.
- **English-only coaching:** Coaching tips are generated in English. Non-English speakers receive less useful guidance.
- **Short context window usage:** Prompts are intentionally minimal to reduce cost and latency. This means Claude cannot do deep multi-turn reasoning about strategy.
- **Evaluator bias:** The reliability evaluator only tests binary search strategy. A human player's random or emotional guessing patterns are not represented.

---

## 🚨 Misuse Considerations

- **Secret number exposure:** The glitch detector prompt includes the secret number. A malicious user who could inspect the prompt could learn the answer. Mitigation: in a production app, glitch analysis should only run post-game, not during.
- **Prompt injection:** A user who submits a very long or malformed guess string could theoretically influence the coaching prompt. Mitigation: `parse_guess()` validates all input before it reaches the AI layer.
- **API cost abuse:** Repeated clicks on "Get Coaching Tip" could generate many API calls. Mitigation: In production, rate limiting and session-level call counts should be enforced.

---

## 🧪 What Surprised Me During Testing

- The binary search agent won **100% of Easy games** every single run — exactly as predicted mathematically. This confirmed the game logic was correct, not just "usually correct."
- Claude occasionally gave coaching tips that assumed the player was trying to lose (e.g., suggesting completely random strategies were "interesting"). Rewriting the prompt to explicitly say "encourage efficient strategy" fixed this.
- The glitch detector confidently flagged correct behavior as a glitch once when I passed it a guess of exactly the boundary value. Prompt clarity around edge cases matters more than I expected.

---

## 🤝 AI Collaboration Notes

### Helpful instance
When writing the `run_reliability_eval` function, Claude suggested using a list comprehension with `simulate_game` rather than a for-loop with manual accumulation. The resulting code was shorter, more readable, and easier to test in isolation. I accepted this suggestion as-is.

### Flawed instance
Claude initially generated a `get_ai_hint` prompt that told the model to "give the player the answer if they are stuck." This was exactly the opposite of what I wanted — it would have made the game trivially easy. I rewrote the prompt to explicitly say "Do not reveal the secret number," which resolved the issue. This reminded me that AI-generated prompts need the same critical review as AI-generated code.

---

## 💭 Reflection

This project taught me that AI systems are only as trustworthy as the constraints you put around them. Claude is capable of excellent coaching and bug detection, but without careful prompt design and input validation, the same capabilities can become liabilities. The most valuable skill I developed was learning to think adversarially about my own system — asking "how could this go wrong?" before shipping each feature. As an AI engineer, my job isn't just to make things work — it's to make them work safely and predictably.
