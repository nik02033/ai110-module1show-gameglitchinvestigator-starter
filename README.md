# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

An AI was asked to build a simple number-guessing game in Streamlit.
It wrote the code, ran away, and left the game completely broken.

- Hints were backwards — guessing too high told you to go higher.
- The score was corrupted by an even/odd parity trick that rewarded wrong guesses.
- The attempt counter started at 1 instead of 0, shifting every win reward down.
- On even-numbered attempts, the secret was silently converted to a string, causing Python to compare numbers alphabetically.

This repo is the fixed version.

---

## 🎯 Game Purpose

Guess a secret number within the allowed number of attempts. Three difficulty levels control the range and attempt limit:

| Difficulty | Range  | Attempts |
|------------|--------|----------|
| Easy       | 1–20   | 6        |
| Normal     | 1–100  | 8        |
| Hard       | 1–50   | 5        |

**Scoring:** Win on attempt 1 for 100 points. Each additional attempt costs 10 points (minimum 10). Each wrong guess costs 5 points.

---

## 🐛 Bugs Found and Fixed

| # | Bug | Location | Fix Applied |
|---|-----|----------|-------------|
| 1 | Hints inverted — "Go HIGHER!" shown when guess was too high | `check_guess` in `app.py` | Swapped the return messages |
| 2 | `try/except TypeError` doing alphabetical string comparison on even attempts | `check_guess` + submit handler | Removed even-attempt `str()` conversion; always compare as integers |
| 3 | Win formula used `attempt_number + 1` (off-by-one) | `update_score` | Changed to `attempt_number - 1` so attempt 1 gives 100 pts |
| 4 | "Too High" on even attempts gave +5 instead of −5 | `update_score` | Unified both wrong-guess outcomes to always deduct 5 |
| 5 | `attempts` initialized to 1 instead of 0 | `app.py` session state | Changed initialization to `0` |
| 6 | `check_guess` and `update_score` were stubs in `logic_utils.py` | `logic_utils.py` | Moved working implementations from `app.py` into `logic_utils.py` |

---

## 🛠️ Setup

```bash
# 1. Activate your conda environment
conda activate base   # or your project env

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Run the app
python -m streamlit run app.py
```

---

## ✅ Running Tests

```bash
python -m pytest tests/test_game_logic.py -v
```

All 14 tests should pass, covering:
- Correct hint direction (too high → go lower, too low → go higher)
- Win scoring at each attempt number
- Consistent 5-point deduction for both "Too High" and "Too Low"

---

## 📁 Project Structure

```
├── app.py              # Streamlit UI and game loop
├── logic_utils.py      # check_guess, update_score (pure logic, no Streamlit)
├── tests/
│   └── test_game_logic.py
├── reflection.md       # Process reflection and lessons learned
└── requirements.txt
```

---

## 📸 Demo

![Fixed game screenshot](Screenshot%202026-03-15%20at%207.09.22%20PM.png)

---

## 🚀 Stretch Features

- [ ] Enhanced Game UI (Challenge 4 screenshot here)
