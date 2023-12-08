import random 
from solver.wordle_color import WordleColor

class Puzzle:
    """
    Represents a wordle puzzle word, which we can query to get an assessment of
    our guess. Also increments guess count every time it's queried. 

    If a word is not explicitly provided, vocab must be provided. 
    In this case, a random word will be chosen from the vocab list.
    """
    assessments = {}
    def __init__(self, word=None, vocab=None) -> None:
        self.vocab = vocab
        if not word:
            if not vocab:
                raise ValueError("Either 'vocab' or 'word' args must be provided.")
            self.word = random.choice(self.vocab)
        else:
            self.word = word
        self.guess_count = 0

    @staticmethod
    def assess_guess(candidate_word, hidden_word):
        """
        Performs a Wordle assess of the candidate_word word vs. the true hidden 
        word. All assessment positions are relative to positions in candidate_word
            - If the letter from candidate_word is in the same position in
            hidden_word, WordleColor.GREEN is returned for that position.
            - If a letter from candidate_word is present in hidden_word but not in
            the same position, WordleColor.YELLOW is returned for that position.
            - If the letter from candidate_word is not present at all in
            hidden_word, WordleColor.BLACK is returned for that position.

        Returns:
            [array] of length(candidate_word) == len(hidden_word), containing
            some combination of WordleColor.BLACK, WordleColor.YELLOW, and
            WordleColor.GREEN
        """
        if (candidate_word, hidden_word) in Puzzle.assessments:
            return Puzzle.assessments[candidate_word, hidden_word]
        hidden_counts = {}
        for idx, _ in enumerate(candidate_word):
            if hidden_word[idx] in hidden_counts:
                hidden_counts[hidden_word[idx]] += 1
            else: 
                hidden_counts[hidden_word[idx]] = 1

        solution = [WordleColor.BLACK] * len(candidate_word)

        # Matches take precedence over present non-matches
        for idx in range(len(candidate_word)):
            candidate_char, hidden_char = candidate_word[idx], hidden_word[idx]
            if candidate_char == hidden_char:
                solution[idx] = WordleColor.GREEN
                hidden_counts[candidate_char] -= 1

        # Check for present in word, but not in current position
        for idx in range(len(candidate_word)):
            candidate_char, hidden_char = candidate_word[idx], hidden_word[idx]
            if solution[idx] != WordleColor.GREEN:
                if candidate_char in hidden_counts:
                    if hidden_counts[candidate_char] > 0:
                        solution[idx] = WordleColor.YELLOW
                
                    hidden_counts[candidate_char] -= 1
        Puzzle.assessments[(candidate_word, hidden_word)] = solution
        return solution

    def assess(self, candidate_word):
        """Performs 'assess_guess' for a specific instance of a puzzle"""
        self.guess_count += 1
        return Puzzle.assess_guess(candidate_word, self.word)

    def get_guess_count(self):
        return self.guess_count
