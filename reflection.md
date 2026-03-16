# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game launched as a number-guessing app with three difficulty settings, but several things were clearly wrong from the start. The hints were backwards (guessing too high told you to go higher), the score jumped around unpredictably, and the attempt counter was off. It felt like a functional-looking app that was quietly broken in multiple places at once.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

1. **Hints were inverted** — `check_guess` returned "Go HIGHER!" when the guess was too high and "Go LOWER!" when it was too low, the exact opposite of correct behavior.
2. **Score was wrong every game** — on even-numbered attempts the secret was secretly converted to a string, causing Python to do a lexicographic comparison (e.g. `"9" > "20"` is True) instead of a numeric one, which corrupted the outcome and therefore the score.
3. **Win reward was off by one attempt** — the formula used `attempt_number + 1` instead of `attempt_number - 1`, so winning on the first try gave 80 points instead of 100.
4. **"Too High" on even attempts gave +5 instead of -5** — the score rewarded wrong guesses depending on a meaningless even/odd parity check.
5. **`attempts` was initialized to 1 instead of 0** and incremented before being passed to `update_score`, which shifted every win reward down by one tier.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Cursor's built-in AI assistant (powered by Claude) throughout this project for reading code, explaining bugs, and applying fixes.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
The AI correctly identified that `check_guess` had inverted return messages and explained exactly why: the `if guess > secret` branch was returning "Go HIGHER!" when the guess was already too big. I verified the fix by running the pytest suite and manually playing a round — after the fix, guessing 80 when the secret was 50 correctly showed "Go LOWER!".

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When I got a score of 45 instead of the expected 40 after winning on attempt 5, the AI initially gave a long speculative explanation involving multiple interacting bugs but couldn't pin down the exact cause with certainty. I had to trace through the code myself to confirm that the even-attempt string conversion was silently skipping a score deduction on one of my wrong guesses, which is what added the extra 5 points.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
A fix was only considered done when both the pytest suite passed and the behavior in the running app matched the expected outcome. For score bugs specifically, I calculated the expected score by hand and compared it to what the app showed.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
I ran `python -m pytest tests/test_game_logic.py -v` after moving `check_guess` and `update_score` into `logic_utils.py`. All 14 tests passed, which confirmed that the refactor hadn't broken any logic and that both the message direction and the score formula were behaving correctly. The test `test_too_high_on_even_attempt_deducts_5` was especially useful — it directly caught the old even/odd bonus bug that would have silently added 5 points instead of subtracting 5.

- Did AI help you design or understand any tests? How?
Yes. The AI wrote the full pytest suite targeting the specific bugs we fixed, grouping them into named classes (`TestCheckGuessMessages`, `TestUpdateScoreWin`, `TestUpdateScoreWrongGuess`) so it was clear which bug each test was catching. It also explained why the existing stub tests were failing with `NotImplementedError` and updated them to unpack the tuple returned by `check_guess`.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Every time the user interacted with the app (clicked a button, changed the difficulty dropdown), Streamlit re-ran the entire Python script from top to bottom. Without `session_state`, `random.randint()` was called fresh every rerun, generating a new secret number each time. The player was essentially chasing a moving target without knowing it.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Imagine your app is a whiteboard that gets completely erased and redrawn every time someone clicks anything. Session state is like a sticky note you put on the side of the whiteboard — it survives the erase. Anything you want to remember between clicks (like the secret number, the score, or the attempt count) has to be written on that sticky note using `st.session_state`.

- What change did you make that finally gave the game a stable secret number?
The secret was already guarded with `if "secret" not in st.session_state` — so it only generates a new random number on the very first run or after "New Game" is pressed. The key issue wasn't the secret changing; it was other values like `attempts` being initialized to `1` instead of `0`, and the even-attempt string conversion making the secret behave differently on alternate turns.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Writing targeted pytest cases immediately after fixing a bug. The act of writing a test that would have caught the original bug (like `test_too_high_on_even_attempt_deducts_5`) forced me to fully understand what was wrong, not just apply a surface-level fix. It also gives future-me a safety net when refactoring.

- What is one thing you would do differently next time you work with AI on a coding task?
I would ask the AI to trace through a specific input end-to-end (e.g. "what is the score after these 5 guesses?") before accepting its explanation of a bug. In this project the AI was occasionally right about the cause but vague about the exact mechanism, and running a concrete example would have surfaced the truth faster.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI-generated code can look completely correct at a glance while hiding subtle, interacting bugs that only appear at runtime under specific conditions — like the even-attempt string conversion that only misbehaved every other guess. I now treat AI-generated logic as a first draft that always needs to be read critically, tested with edge cases, and verified against expected outputs.
