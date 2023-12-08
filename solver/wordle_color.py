# Drop-in replacement to considerably speed up enum comparisons
import fastenum

class WordleColor(fastenum.Enum):
    """
    Enum for colors corresponding to Wordle puzzle info

    BLACK: guessed letter in this position is not in the hidden word
    YELLOW: guessed letter in this position is in the hidden word, but not in this position
    GREEN: guessed letter in this position is in the hidden word, also in this position
    """
    BLACK = 0
    YELLOW = 1
    GREEN = 2
