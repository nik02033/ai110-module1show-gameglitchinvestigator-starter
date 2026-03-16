import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from logic_utils import check_guess, update_score

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests targeting fixed bugs ---

# Bug 1: check_guess returned inverted messages ("Go HIGHER!" when guess was
# too high, "Go LOWER!" when guess was too low).
class TestCheckGuessMessages:
    def test_too_high_message_says_go_lower(self):
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"
        assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message}"

    def test_too_low_message_says_go_higher(self):
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message}"

    def test_correct_guess_message(self):
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert "Correct" in message


# Bug 2a: update_score win formula used attempt_number + 1 instead of
# attempt_number - 1, so a first-attempt win gave 80 instead of 100.
class TestUpdateScoreWin:
    def test_win_on_attempt_1_gives_100_points(self):
        score = update_score(0, "Win", 1)
        assert score == 100

    def test_win_on_attempt_2_gives_90_points(self):
        score = update_score(0, "Win", 2)
        assert score == 90

    def test_win_on_attempt_10_floors_at_10_points(self):
        score = update_score(0, "Win", 10)
        assert score == 10

    def test_win_adds_to_existing_score(self):
        score = update_score(50, "Win", 1)
        assert score == 150


# Bug 2b: "Too High" on even attempts rewarded +5 instead of deducting 5,
# creating an inconsistency with "Too Low" which always deducted 5.
class TestUpdateScoreWrongGuess:
    def test_too_high_on_even_attempt_deducts_5(self):
        score = update_score(50, "Too High", 2)
        assert score == 45, "Too High on even attempt should deduct 5, not add 5"

    def test_too_high_on_odd_attempt_deducts_5(self):
        score = update_score(50, "Too High", 3)
        assert score == 45

    def test_too_low_deducts_5(self):
        score = update_score(50, "Too Low", 1)
        assert score == 45

    def test_too_high_and_too_low_penalise_equally(self):
        score_high = update_score(50, "Too High", 2)
        score_low = update_score(50, "Too Low", 2)
        assert score_high == score_low, "Too High and Too Low should deduct the same points"
