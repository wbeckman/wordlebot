import pytest
import information
from wordle_color import WordleColor


@pytest.fixture
def all_different_vocab():
    return [
        'AAAAA',
        'BBBBB',
        'CCCCC',
        'DDDDD'
    ]

@pytest.fixture
def clear_winner_vocab():
    return [
        'ABCD',
        'AAAA',
        'BBBB',
        'CCCC',
        'DDDD'
    ]

def test_compute_pattern_frequencies_all_different(all_different_vocab):
    """
    Test functionality of compute_pattern_frequencies on alphabet where
    no words provides any information about any other word
    """
    expected = {
        'AAAAA': {
            tuple([WordleColor.GREEN] * 5): set(['AAAAA']), 
            tuple([WordleColor.BLACK] * 5): set(['BBBBB', 'CCCCC', 'DDDDD'])},
        'BBBBB': {
            tuple([WordleColor.GREEN] * 5): set(['BBBBB']), 
            tuple([WordleColor.BLACK] * 5): set(['AAAAA', 'CCCCC', 'DDDDD'])},
        'CCCCC': {
            tuple([WordleColor.GREEN] * 5): set(['CCCCC']), 
            tuple([WordleColor.BLACK] * 5): set(['AAAAA', 'BBBBB', 'DDDDD'])},
        'DDDDD': {
            tuple([WordleColor.GREEN] * 5): set(['DDDDD']), 
            tuple([WordleColor.BLACK] * 5): set(['AAAAA', 'BBBBB', 'CCCCC'])}
    }
    assert information.compute_pattern_frequencies(all_different_vocab, all_different_vocab) == expected

def test_compute_pattern_frequencies_clear_winner(clear_winner_vocab):
    """
    Test functionality of compute_pattern_frequencies on alphabet where
    there is one word that is clearly the best
    """
    expected = {
        'ABCD': {
            tuple([WordleColor.GREEN] * 4): set(['ABCD']), 
            tuple([WordleColor.BLACK] * 3 + [WordleColor.GREEN]): set(['DDDD']),
            tuple([WordleColor.BLACK] * 2 + [WordleColor.GREEN, WordleColor.BLACK]): set(['CCCC']),
            tuple([WordleColor.BLACK, WordleColor.GREEN] + [WordleColor.BLACK] * 2 ): set(['BBBB']),
            tuple([WordleColor.GREEN] + [WordleColor.BLACK] * 3): set(['AAAA']),
        },
        'AAAA': {
            tuple([WordleColor.GREEN] * 4): set(['AAAA']),
            tuple([WordleColor.BLACK] * 4): set(['BBBB', 'CCCC', 'DDDD']),
            tuple([WordleColor.GREEN] + [WordleColor.BLACK] * 3): set(['ABCD'])
        },
        'BBBB': {
            tuple([WordleColor.GREEN] * 4): set(['BBBB']),
            tuple([WordleColor.BLACK] * 4): set(['AAAA', 'CCCC', 'DDDD']),
            tuple([WordleColor.BLACK, WordleColor.GREEN] + [WordleColor.BLACK] * 2): set(['ABCD'])
        },
        'CCCC': {
            tuple([WordleColor.GREEN] * 4): set(['CCCC']),
            tuple([WordleColor.BLACK] * 4): set(['AAAA', 'BBBB', 'DDDD']),
            tuple([WordleColor.BLACK] * 2 + [WordleColor.GREEN, WordleColor.BLACK]): set(['ABCD'])
        },
        'DDDD': {
            tuple([WordleColor.GREEN] * 4): set(['DDDD']),
            tuple([WordleColor.BLACK] * 4): set(['AAAA', 'BBBB', 'CCCC']),
            tuple([WordleColor.BLACK] * 3 + [WordleColor.GREEN]): set(['ABCD'])
        }
    }
    assert information.compute_pattern_frequencies(clear_winner_vocab, clear_winner_vocab) == expected

def test_compute_information_all_different(all_different_vocab):
    pattern_frequencies = information.compute_pattern_frequencies(all_different_vocab, all_different_vocab)
    
    # Hand-calculated information values
    expected = {
        'AAAAA': 0.8112781244591327,
        'BBBBB': 0.8112781244591327,
        'CCCCC': 0.8112781244591327,
        'DDDDD': 0.8112781244591327
    }
    info = information.compute_information_from_frequencies(pattern_frequencies, all_different_vocab)
    assert info == expected

def test_compute_information_clear_winner(clear_winner_vocab):
    pattern_frequencies = information.compute_pattern_frequencies(clear_winner_vocab, clear_winner_vocab)
    
    # Hand-calculated information values
    expected = {
        'ABCD': 2.321928094887362,
        'AAAA': 1.3709505944546687,
        'BBBB': 1.3709505944546687,
        'CCCC': 1.3709505944546687,
        'DDDD': 1.3709505944546687
    }
    info = information.compute_information_from_frequencies(pattern_frequencies, clear_winner_vocab)
    assert info == expected


def test_compute_information_subset(clear_winner_vocab):
    alphabet_subset = ['AAAA', 'BBBB']
    pattern_frequencies = information.compute_pattern_frequencies(clear_winner_vocab, alphabet_subset)
    print(pattern_frequencies)

    
    # Hand-calculated information values
    expected = {
        'ABCD': 0.9287712379549449,
        'AAAA': 0.9287712379549449,
        'BBBB': 0.9287712379549449,
        'CCCC': 0.528771237954945,
        'DDDD': 0.528771237954945
    }
    info = information.compute_information_from_frequencies(pattern_frequencies, clear_winner_vocab)
    print(info)
    assert info == expected
