
import streamlit as st
import random
from dotenv import load_dotenv
load_dotenv()
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)
from ai_coach import get_ai_hint, get_glitch_analysis
from evaluator import run_reliability_eval
from logger import setup_logger, log_event

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

# --- Logger setup ---
logger = setup_logger("game_log.txt")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game — now with an AI coach.")

# --- Tabs ---
tab_game, tab_coach, tab_eval = st.tabs(["🎮 Game", "🤖 AI Coach", "📊 Reliability Report"])


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


# ============================================================
# SESSION STATE
# ============================================================
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
    log_event(logger, "GAME_START", {"difficulty": difficulty, "secret": st.session_state.secret})

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "outcomes" not in st.session_state:
    st.session_state.outcomes = []

if "coach_tip" not in st.session_state:
    st.session_state.coach_tip = ""

if "glitch_report" not in st.session_state:
    st.session_state.glitch_report = ""


# ============================================================
# TAB 1 — GAME
# ============================================================
with tab_game:
    st.subheader("Make a guess")

    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )

    raw_guess = st.text_input("Enter your guess:")
    submit = st.button("Submit Guess 🚀")
    new_game = st.button("New Game 🔁")

    if new_game:
        st.session_state.clear()
        log_event(logger, "NEW_GAME", {"difficulty": difficulty})
        st.rerun()

    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success(
                f"🎉 You won! Secret: {st.session_state.secret} | "
                f"Score: {st.session_state.score}"
            )
        else:
            st.error(
                f"💀 Game over! Secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )
    else:
        if submit:
            # UPDATED: We now pass low and high to the validator
            ok, guess, err = parse_guess(raw_guess, low, high)

            if not ok:
                st.error(err)
                log_event(logger, "INVALID_GUESS", {"raw": raw_guess, "error": err})
            else:
                st.session_state.attempts += 1
                st.session_state.history.append(guess)

                outcome, message = check_guess(guess, st.session_state.secret)
                st.session_state.outcomes.append(outcome)
                st.warning(message)

                st.session_state.score = update_score(
                    st.session_state.score, outcome, st.session_state.attempts
                )

                log_event(logger, "GUESS", {
                    "guess": guess,
                    "secret": st.session_state.secret,
                    "outcome": outcome,
                    "attempts": st.session_state.attempts,
                    "score": st.session_state.score,
                })

                if outcome == "Win":
                    st.session_state.status = "won"
                    st.balloons()
                    st.success(
                        f"You won! Secret: {st.session_state.secret} | "
                        f"Score: {st.session_state.score}"
                    )
                    log_event(logger, "WIN", {
                        "secret": st.session_state.secret,
                        "attempts": st.session_state.attempts,
                        "score": st.session_state.score,
                    })

                elif st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(
                        f"Game over! Secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )
                    log_event(logger, "LOSS", {
                        "secret": st.session_state.secret,
                        "attempts": st.session_state.attempts,
                        "score": st.session_state.score,
                    })

    # Guess history
    if st.session_state.history:
        st.markdown("**Guess history:** " + ", ".join(str(g) for g in st.session_state.history))


# ============================================================
# TAB 2 — AI COACH
# ============================================================
with tab_coach:
    st.subheader("🤖 AI Strategy Coach")
    st.write("Get real-time coaching on your guessing strategy from Claude.")

    if st.button("Get Coaching Tip"):
        if not st.session_state.history:
            st.warning("Make at least one guess first!")
        else:
            with st.spinner("Asking Claude..."):
                tip = get_ai_hint(
                    st.session_state.history,
                    low,
                    high,
                    st.session_state.attempts,
                )
                st.session_state.coach_tip = tip
                log_event(logger, "AI_COACH_CALLED", {
                    "attempts": st.session_state.attempts,
                    "history": st.session_state.history,
                })

    if st.session_state.coach_tip:
        st.info(st.session_state.coach_tip)

    st.divider()
    st.subheader("🔍 Glitch Detector")
    st.write("Ask Claude to review your hint history and flag any logic errors.")

    if st.button("Run Glitch Analysis"):
        if not st.session_state.history:
            st.warning("Make at least one guess first!")
        else:
            with st.spinner("Analyzing game logic..."):
                report = get_glitch_analysis(
                    st.session_state.history,
                    st.session_state.outcomes,
                    st.session_state.secret,
                )
                st.session_state.glitch_report = report
                log_event(logger, "GLITCH_ANALYSIS", {
                    "history": st.session_state.history,
                    "outcomes": st.session_state.outcomes,
                })

    if st.session_state.glitch_report:
        st.info(st.session_state.glitch_report)


# ============================================================
# TAB 3 — RELIABILITY REPORT
# ============================================================
with tab_eval:
    st.subheader("📊 Reliability Evaluator")
    st.write(
        "Simulate hundreds of games automatically using a binary search strategy "
        "and measure how reliably the game logic performs."
    )

    eval_difficulty = st.selectbox("Difficulty to evaluate:", ["Easy", "Normal", "Hard"])
    n_games = st.slider("Number of simulated games:", min_value=50, max_value=500, value=100, step=50)

    if st.button("Run Evaluation"):
        with st.spinner(f"Simulating {n_games} games..."):
            stats = run_reliability_eval(n=n_games, difficulty=eval_difficulty)
            log_event(logger, "EVAL_RUN", stats)

        st.success("Evaluation complete!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Win Rate", f"{stats['win_rate_pct']}%")
        col2.metric("Avg Attempts", stats['avg_attempts'])
        col3.metric("Avg Score", stats['avg_score'])

        st.markdown(f"""
**Summary:** Out of **{stats['total_games']}** simulated games on **{eval_difficulty}** difficulty:
- ✅ Wins: {stats['wins']}
- ❌ Losses: {stats['losses']}
- 📈 Win Rate: {stats['win_rate_pct']}%
- 🎯 Average attempts to win: {stats['avg_attempts']}
- 💯 Average score: {stats['avg_score']}
        """)
