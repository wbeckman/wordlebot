```
 __      __ ___   ___  ___   _     ___  ___   ___  _____
 \ \    / // _ \ | _ \|   \ | |   | __|| _ ) / _ \|_   _|
  \ \/\/ /| (_) ||   /| |) || |__ | _| | _ \| (_) | | |
   \_/\_/  \___/ |_|_\|___/ |____||___||___/ \___/  |_|
```

Welcome to the repo for `wordlebot` - my wordle-playing bot that relies on the concept of entropy to solve New York Times Wordle puzzles. If you want a breakdown of how it works, I wrote a [blog post](https://willbeckman.com/wordle.html) on that.

### Implementation

In a few sentences, it computes the entropy for all words in the vocab against all words that could possibly be a solution on the New York Times' (NYT) word lists. Then, if there is a tie between multiple best words, it recommends a word that is in the possible hidden words solution set.

### CLI

There is a pip-installable CLI that goes along with this solver. If you clone this repo with:

```git clone git@github.com:wbeckman/wordlebot.git```

and then CD into the wordlebot folder

```cd wordlebot```

you can pip install the bot into your current environment with the following command (you can create a virtual environment if you don't want it installed on your global system python):

```pip install .```

You can now invoke the bot using the terminal command `wordlebot`.

### Notes on Usage

The bot tells you how to play, but in case you're curious, I will paste an example session here

```
➜  ~ wordlebot
 __      __ ___   ___  ___   _     ___  ___   ___  _____
 \ \    / // _ \ | _ \|   \ | |   | __|| _ ) / _ \|_   _|
  \ \/\/ /| (_) ||   /| |) || |__ | _| | _ \| (_) | | |
   \_/\_/  \___/ |_|_\|___/ |____||___||___/ \___/  |_|

(Press CTRL+C to exit at any time)

Your first guess to maximize the amount of information you gain on average should always be 'TARSE'.
However, you're free to guess whatever you want.

Give me your guess and the feedback you received, and I can tell you what to guess next to minimize your number of guesses, on average.


**********GUESS 1**********
Tell me what you guessed: RAISE
You guessed: RAISE.
Am I understanding that correctly? (type y/n): y


Tell me what the feedback was from the wordle puzzle.
Use the letters: 'G', 'Y', 'B' in order to denote the colors [GREEN, YELLOW, BLACK]: ybbyb
You learned: 🟨 ⬛ ⬛ 🟨 ⬛ .
Am I understanding that correctly? (type y/n): y
Computing information... \
Done!

Your guess shrunk the search space from 2309 to 24 (a factor of 96.20833333333333)
Based on your guess and the feedback received, I would recommend guessing 'POYNT' next.
On average, this will reduce the search space of 24 remaining words to roughly 1/13 of what it was.
Other good guesses would be:
	Word: poynt;	 Search space reduction (on average): 1 / 13.962727235148423
	Word: chout;	 Search space reduction (on average): 1 / 13.179059572237678
	Word: count;	 Search space reduction (on average): 1 / 13.179059572237678
	Word: thorp;	 Search space reduction (on average): 1 / 12.89483918188251
	Word: thrum;	 Search space reduction (on average): 1 / 12.89483918188251

**********GUESS 2**********
Tell me what you guessed: POYNT
You guessed: POYNT.
Am I understanding that correctly? (type y/n): y


Tell me what the feedback was from the wordle puzzle.
Use the letters: 'G', 'Y', 'B' in order to denote the colors [GREEN, YELLOW, BLACK]: bybyg
You learned: ⬛ 🟨 ⬛ 🟨 🟩 .
Am I understanding that correctly? (type y/n): y
Computing information... |
Based on what you guessed, there could only possibly be one word left. That word is SNORT.
You should solve this puzzle in exactly 3 turns. Congrats!
Do another? (y/n): n
See you soon!
```

This is, of course, cherry-picked to include an example where the bot solves the puzzle in three turns ;). Don't ask me what "POYNT" means. Ask the NYT.

Note - [wordle unlimited](https://wordleunlimited.org/) uses a very similar vocabulary to my bot, but the 'best' word "TARSE" is not present in its vocab. If you want to test this bot on the Wordle unlimited website, you will have to open with another word ('RAISE' and 'TARES' are both solid words).


### Performance

If you're using the NYT official hidden words list, this bot has a performance of 3.61 guesses on average on that list. Pretty good, almost certainly better than average human play, but not optimal. An optimal bot would look ahead with a tree search to produce optimal estimates. This bot is just based on an entropy heuristic and definitely overfitted to a small selection of words (2309) that the NYT has chosen as its possible solutions list.
