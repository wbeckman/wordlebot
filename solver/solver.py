from solver.wordle_color import WordleColor
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
