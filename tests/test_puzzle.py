from solver.puzzle import Puzzle
from solver.wordle_color import WordleColor


def test_assess():
    """Test basic functionality of assess on no special case"""
    candidate_word = 'wings'
    expected = [WordleColor.GREEN, WordleColor.YELLOW, WordleColor.BLACK, WordleColor.BLACK, WordleColor.YELLOW]
    puzzle = Puzzle('waist')
    assert puzzle.assess(candidate_word) == expected

def test_assess_multiple_letters_hidden():
    """
    There are two 'a's in the hidden word. If we guess one 'a', it should not
    give away that there is more than one 'a'
    """
    candidate_word = 'spark'
    expected = [
        WordleColor.BLACK, WordleColor.YELLOW, WordleColor.YELLOW, WordleColor.BLACK, WordleColor.BLACK
    ]
    puzzle = Puzzle('panda')
    assert puzzle.assess(candidate_word) == expected

def test_assess_multiple_letters_candidate():
    """
    There are two 'a's in the candidate word, but only one in the hidden word.
    In this case, the first 'a' should be green/yellow and the second should be BLACK.
    """
    candidate_word = 'panda'
    puzzle = Puzzle('spark')
    expected = [
        WordleColor.YELLOW, WordleColor.YELLOW, WordleColor.BLACK, WordleColor.BLACK, WordleColor.BLACK
    ]
    assert puzzle.assess(candidate_word) == expected

def test_assess_green_priority():
    """
    There is one 'a', but in this case, the green 'a' has precedence over the yellow 'a'
    """
    candidate_word = 'panda'
    puzzle = Puzzle('sigma')
    expected = [
        WordleColor.BLACK, WordleColor.BLACK, WordleColor.BLACK, WordleColor.BLACK, WordleColor.GREEN
    ]
    assert puzzle.assess(candidate_word) == expected
