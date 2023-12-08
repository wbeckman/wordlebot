from solver.puzzle import Puzzle

class AssessSolver:
    def __init__(self, vocab) -> None:
        self.vocab = vocab

    def _print_if_verbose(self, str, verbose):
        if verbose:
            print(str)

    def assess(self, solver, verbose=False):
        """
        Assesses a solver's performance on the vocabulary (must be a subset
        of the solver's vocabulary)
        """
        sum_guesses = 0
        guesses_over_six = []
        all_guesses = {}
        for word in self.vocab:
            puzzle = Puzzle(word=word)
            self._print_if_verbose(f'Word: {word}', verbose)
            guesses = solver.solve(puzzle)
            all_guesses[word] = guesses
            self._print_if_verbose(f'Guesses: {guesses}', verbose)
            num_guesses = puzzle.get_guess_count()
            sum_guesses += num_guesses
            if num_guesses > 6:
                self._print_if_verbose(f'*******{word} over 6 guesses!*******', verbose)
                guesses_over_six.append(word)
            
        avg_guess_count = sum_guesses / len(self.vocab)
        self._print_if_verbose(f'Num guesses on average: {sum_guesses / len(self.vocab)}', verbose)
        self._print_if_verbose(f'Num guesses over six: {len(guesses_over_six)}', verbose)
        self._print_if_verbose(f'Words over six guesses: {guesses_over_six}', verbose)

        # Return average num guesses
        return all_guesses