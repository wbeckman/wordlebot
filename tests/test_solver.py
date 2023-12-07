import pytest
from puzzle import Puzzle
import solver

@pytest.fixture
def chimp_vocab():
    return [
        'CHIMP',
        'CATCH',
        'PATCH',
        'MATCH',
        'HATCH'
    ]

def test_info_theory_solver_chimp(chimp_vocab):
    """
    Tests functionality of information theory solver. For the word "chimp",
    the solver should solve the puzzle on its first try. 
    """
    puzzle = Puzzle('CHIMP')
    info_theory_solver = solver.InformationTheorySolver(chimp_vocab, chimp_vocab)
    guesses = info_theory_solver.solve(puzzle)
    assert puzzle.get_guess_count() == 1
    assert guesses == ['CHIMP']

def test_info_theory_solver_catch(chimp_vocab):
    """
    Tests functionality of information theory solver
    """
    puzzle = Puzzle('CATCH')
    info_theory_solver = solver.InformationTheorySolver(chimp_vocab, chimp_vocab)
    guesses = info_theory_solver.solve(puzzle)
    assert puzzle.get_guess_count() == 2
    assert guesses == ['CHIMP', 'CATCH']

def test_info_theory_solver_patch(chimp_vocab):
    """
    Tests functionality of information theory solver
    """
    puzzle = Puzzle('PATCH')
    info_theory_solver = solver.InformationTheorySolver(chimp_vocab, chimp_vocab)
    guesses = info_theory_solver.solve(puzzle)
    assert puzzle.get_guess_count() == 2
    assert guesses == ['CHIMP', 'PATCH']

def test_info_theory_solver_match(chimp_vocab):
    """
    Tests functionality of information theory solver
    """
    puzzle = Puzzle('MATCH')
    info_theory_solver = solver.InformationTheorySolver(chimp_vocab, chimp_vocab)
    guesses = info_theory_solver.solve(puzzle)
    assert puzzle.get_guess_count() == 2
    assert guesses == ['CHIMP', 'MATCH']
