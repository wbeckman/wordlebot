import pickle
from solver.wordle_color import WordleColor
from solver.assess_solver import AssessSolver
import random
import abc
import solver.information as information


class InformationBasedSolver(object, metaclass=abc.ABCMeta):
    """
    A wordle solver that makes use of information in its solution. Includes
    checking for pre-computed information in constructor (and computing it
    if a path is not provided - NOTE - this takes a while).
    """
    def __init__(self, vocab, possible_solutions, pattern_path=None, information_path=None):
        self.vocab = vocab
        # This is all for the purpose of avoiding the expensive operation of computing information
        # for the entire vocab
        self.possible_solutions = possible_solutions
        pattern_path_without_information_path = pattern_path is not None and information_path is None
        information_path_without_pattern_path = pattern_path is None and information_path is not None
        if pattern_path_without_information_path or information_path_without_pattern_path:
            raise ValueError("If one of [information_path, pattern_path] is provided, " + \
                             "the other must be provided as well.")
        if information_path:
            self.pattern_frequencies = information.compute_pattern_frequencies(
                vocab, vocab, pattern_path)
            self.information = information.compute_information_from_frequencies(
                self.pattern_frequencies, vocab, information_path)
        else:
            self.pattern_frequencies = information.compute_pattern_frequencies(
                vocab, vocab)
            self.information = information.compute_information_from_frequencies(
                self.pattern_frequencies, vocab)

    @abc.abstractmethod
    def get_guess(self, word_information):
        pass

    def solve(self, puzzle):
        """
        Function stub to solve inputted puzzle. Implementation
        depends on subclass.

        :param puzzle:
            Puzzle object that we wish to solve with the given solver.
        """
        correct_sol = [WordleColor.GREEN] * 5
        assessment = None
        guesses = []
        possible_vocab = set(self.possible_solutions)
        pattern_frequencies = self.pattern_frequencies
        word_information = self.information
        while assessment != correct_sol:
            guess = self.get_guess(word_information)
            guesses.append(guess)
            assessment = puzzle.assess(guess)
            
            # Subset vocab to only what is possible based on feedback
            possible_vocab = possible_vocab.intersection(set(self.filter_on_assessment(guess, assessment))) - set(guesses)
            if assessment == correct_sol: break
            if len(possible_vocab) == 1:
                puzzle.assess(guess)
                guesses.append(list(possible_vocab)[0])
                break
            pattern_frequencies = information.compute_pattern_frequencies(self.vocab, possible_vocab)
            word_information = information.compute_information_from_frequencies(pattern_frequencies, possible_vocab)
            for g in guesses:
                del word_information[g]
        
        return guesses

    def filter_on_assessment(self, guessed_word, assessment):
        """
        Filters vocab based on which words could be possible, given
        a guessed word and an assessment of that guessed word.
        """
        return list(self.pattern_frequencies[guessed_word][tuple(assessment)])

class InformationTheorySolver(InformationBasedSolver):
    """
    Solves purely based on information criteria. Much more likely
    to narrow the guesses down to exactly one choice, since it typically 
    guesses uncommon words.
    """
    def __init__(self, vocab, possible_solutions, pattern_path=None, information_path=None) -> None:
        super().__init__(vocab, possible_solutions, pattern_path, information_path)

    def get_guess(self, word_information):
        """Returns guess containing most information"""
        return max(word_information, key=word_information.get)

def load_vocab_file(path):
    with open(path, 'r', encoding='UTF-8') as file:
        vocab = [w.strip() for w in file.readlines()]
    return vocab

def main():
    # Reset random seed
    random.seed=42

    # Wordle lists were taken from Alex Selby (https://github.com/alex1770)
    # Who, in turn, took them from the NYT front-end
    official_words_path = 'official_words.txt'
    hidden_words_path = 'hidden_words.txt'
    
    pattern_frequencies_path = 'pattern_frequencies_all_words_hidden_words.pkl'
    information_path='information_all_words_hidden_words.pkl'
    
    all_vocab = load_vocab_file(official_words_path)
    potential_hidden_words = load_vocab_file(hidden_words_path)

    # Computes top common words - cached info/pattern frequency data
    info_solver = InformationTheorySolver(all_vocab, potential_hidden_words,
        pattern_path=pattern_frequencies_path, information_path=information_path)
    
    common_assessor = AssessSolver(potential_hidden_words)
    guesses = common_assessor.assess(info_solver, verbose=True)
    
    # Reminder - CHANGE THESE NAMES in the morning
    with open('info_theory_guesses.pkl', 'wb') as handle:
        pickle.dump(guesses, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('info_theory_guesses.pkl', 'rb') as handle:
        f = pickle.load(handle)
    
    # Print longest guess strings
    print(sorted(f.items(), key=lambda x: len(x[1]))[-40:])


if __name__ == '__main__':
    import cProfile
    cProfile.run('main()')

    # Info solver, utilizing two separate word lists:
    # Num guesses on average: 3.6440017323516676
    # Num guesses over six: 0
    # Words over six guesses: []

    # IF we wanted to re-generate pattern frequencies/information calculations
    # official_words_path = 'official_words.txt'
    # hidden_words_path = 'hidden_words.txt'
    # vocab = load_vocab_file(official_words_path)
    # hidden_words = load_vocab_file(hidden_words_path)
    # pattern_frequencies = information.compute_pattern_frequencies(
    #     vocab, vocab)
    # information = information.compute_information_from_frequencies(
    #     pattern_frequencies, vocab)


    # with open('pattern_frequencies_all_words_hidden_words.pkl', 'wb') as handle:
    #     pickle.dump(pattern_frequencies, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('information_all_words_hidden_words.pkl', 'wb') as handle:
    #     pickle.dump(information, handle, protocol=pickle.HIGHEST_PROTOCOL)
