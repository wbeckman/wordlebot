import pickle
import random
from solver import assess_solver
import solver.solver


def main():
    # Reset random seed
    random.seed=42

    # Wordle lists were taken from Alex Selby (https://github.com/alex1770)
    # Who, in turn, took them from the NYT front-end
    official_words_path = 'solver/official_words.txt'
    hidden_words_path = 'solver/hidden_words.txt'
    
    pattern_frequencies_path = 'pattern_frequencies_all_words_hidden_words.pkl'
    information_path='information_all_words_hidden_words.pkl'
    
    all_vocab = solver.solver.load_vocab_file(official_words_path)
    potential_hidden_words = solver.solver.load_vocab_file(hidden_words_path)

    # Computes top common words - cached info/pattern frequency data
    info_solver = solver.solver.InformationTheorySolver(all_vocab, potential_hidden_words,
        pattern_path=pattern_frequencies_path, information_path=information_path)
    
    common_assessor = assess_solver.AssessSolver(potential_hidden_words)
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
    # Num guesses on average: 3.608921611087051
    # Num guesses over six: 0
    # Words over six guesses: []

    # IF we wanted to re-generate pattern frequencies/information calculations
    # official_words_path = 'solver/official_words.txt'
    # hidden_words_path = 'solver/hidden_words.txt'
    # vocab = solver.solver.load_vocab_file(official_words_path)
    # hidden_words = solver.solver.load_vocab_file(hidden_words_path)
    # pattern_frequencies = information.compute_pattern_frequencies(
    #     vocab, hidden_words)
    # information = information.compute_information_from_frequencies(
    #     pattern_frequencies, vocab)

    # with open('pattern_frequencies_all_words_hidden_words.pkl', 'wb') as handle:
    #     pickle.dump(pattern_frequencies, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('information_all_words_hidden_words.pkl', 'wb') as handle:
    #     pickle.dump(information, handle, protocol=pickle.HIGHEST_PROTOCOL)
