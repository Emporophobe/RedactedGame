from __future__ import print_function
from Censor import *


class Game:
    """
    Handle user interaction and manage difficulty settings.

    This class handles displaying the headlines and recording users' attempts to guess the search term
    """
    _topic_list = []
    _random_censoring_proportion = 0
    _num_headlines = 0
    _guesses = 0
    _censor = Censor()

    def __init__(self, topics_file, random_censoring=0.1, num_headlines=10, guesses=1):
        """
        Initialize the Game with the given settings.

        This initializer will attempt to fix parameter values which are out of their acceptable ranges
        :param topics_file: The file containing the list of topics (One single-word topic per line)
        :param random_censoring: The proportion [0, 1] of words to randomly censor (higher is more difficult)
        :param num_headlines: The number of headlines [1, 10] to display. API limit means 10 is the max.
        :param guesses: How many bad guesses (>= 1) to allow before failure.
        """
        with open(topics_file, 'r') as f:
            self._topic_list = f.read().splitlines()
        self._random_censoring_proportion = random_censoring
        self._num_headlines = num_headlines
        self._guesses = guesses

        # Fix any bad values
        if self._random_censoring_proportion < 0:
            self._random_censoring_proportion = 0
        elif self._random_censoring_proportion > 1:
            self._random_censoring_proportion = 1

        if self._num_headlines < 1:
            self._num_headlines = 1
        # We only get 10 headlines per API call
        elif self._num_headlines > 10:
            self._num_headlines = 10

        if self._guesses < 1:
            self._guesses = 1

    def new_round(self, topic, display_headline, prompt_for_guess, on_correct_guess, on_bad_guess, on_loss):
        """
        Play a single round of the game.

        This function takes a number of function arguments in order to easily adapt to different user interfaces
        e.g. passing print functions in to play in console, or passing in tkinter-based calls for a basic game GUI

        :param topic: The search query/answer
        :param display_headline: (Str -> None) Display a single headline string
        :param prompt_for_guess: (None -> Str) Prompt the user for a guess and passes it to the function as a string
        :param on_correct_guess: (None -> None) What to do when the user guesses correctly
        :param on_bad_guess: (None -> None) What to do when the user guesses incorrectly
        :param on_loss: (None -> None) What to do when the user runs out of guesses
        :return: Whether the user's guess was correct.
        """
        headlines = self._censor.create_censored_headlines(topic, self._random_censoring_proportion)

        for headline in random.sample(headlines, max(self._num_headlines, len(headlines))):
            display_headline(headline)
        won = False
        for i in xrange(self._guesses):
            guess = prompt_for_guess()
            if guess.lower() == topic.lower():
                on_correct_guess()
                won = True
                break
            else:
                on_bad_guess()
                continue
        if not won:
            on_loss()
        return won

    def new_terminal_round(self, topic):
        """
        Create a version of new_round that interacts with the user via terminal
        :param topic: The search query/answer
        :return: Whether the user guessed correctly
        """
        return self.new_round(
            topic,
            print,
            lambda: raw_input("> " if len(topic.split()) == 1 else "{0} words > ".format(len(topic.split()))),
            lambda: print("yay"),
            lambda: print("boo"),
            lambda: print("Answer: {0}".format(topic))
        )

    def play_in_terminal(self, rounds):
        """
        Play a set number of rounds in the terminal
        :param rounds:
        :return:
        """
        # sample topics without replacement so we don't see the same headlines twice in a game
        topics = random.sample(self._topic_list, min(len(self._topic_list), rounds))
        won = 0
        for topic in topics:
            if self.new_terminal_round(topic):
                won += 1
        return won


def main():
    """
    Play the game.

    This will probably eventually be replaced with a better user interface
    :return: None
    """
    g = Game("topics.txt")
    rounds = 5
    won = g.play_in_terminal(rounds)
    print("{0}/{1} correct".format(won, rounds))
    raw_input()  # Keep from exiting immediately

if __name__ == "__main__":
    main()
