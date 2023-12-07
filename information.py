import math
import pickle
from collections import defaultdict
from puzzle import Puzzle


def compute_pattern_frequencies(original_vocab, subset_vocab, path=None):
    """
    Computes the frequencies with which a pattern occurs. Namely, given
    a vocabulary [word1, word2, word2, ..., word_n], this function computes
    a dictionary of dictionaries, showing how frequently a pattern occurs
    (and which words are contained within this pattern.
    
    It produces a dictionary which looks as follows:
    {
        word1: {
            [WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN]: {word1},
            [WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN, WordleColor.BLACK]: {word2, word2, ...},
            ...
        }, ...
    }
    """
    if path:
        with open(path, 'rb') as handle:
            pattern_frequencies = pickle.load(handle)
        return pattern_frequencies
    pattern_frequencies = {}
    for word in original_vocab:
        pattern_frequencies[word] = {}
        for other in subset_vocab:
            assessment = tuple(Puzzle.assess_guess(word, other))
            if assessment not in pattern_frequencies[word]:
                pattern_frequencies[word][assessment] = set([other])
            else:
                pattern_frequencies[word][assessment].add(other)
    return pattern_frequencies

def compute_information_from_frequencies(pattern_frequencies, subsetted_vocab, path=None):
    """
    Given a dictionary of dictionaries in the format:
    {
        word1: {
            [WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN]: {word1},
            [WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN, WordleColor.GREEN, WordleColor.BLACK]: {word2, word2, ...},
            ...
        }, ...
    }

    This function computes the information for the top-level words in the
    dictionary. This is based on the expected size of a "subset" after
    choosing a word, based on all available subsets for that word.

    Information is computed as negative entropy: E(I) = \sum_x{P(x) * log_2{1/P(x)}}

    Where P(x) is the probability of a particular pattern occurring

    Will also load a cached list if a file path is provided (using pickle, loading binary)
    """
    if path:
        with open(path, 'rb') as handle:
            info = pickle.load(handle)
        return info
    # vocab = list(pattern_frequencies.keys())
    num_vocab_inv = (1 / len(subsetted_vocab))
    expected_information = {}
    # We want to compute information for ALL words in pattern_frequencies,
    # regardless of whether they are still in 'vocab'
    for word in pattern_frequencies.keys():
        for pattern, other_words in pattern_frequencies[word].items():
            probability = len(other_words) * num_vocab_inv
            if word in expected_information:
                expected_information[word] += probability * math.log(1/probability, 2)
            else:
                expected_information[word] = probability * math.log(1/probability, 2)
    return expected_information