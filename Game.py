from Censor import *
import random


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

    def new_round(self):
        """
        Play a single round of the game.

        Generate and print headlines based on one of the topics in the topics file
        and display censored versions of the headlines. Prompt user for their guess of what the search term was.
        :return: Whether the user's guess was correct.
        """
        topic = random.choice(self._topic_list)
        headlines = self._censor.create_censored_headlines(topic, self._random_censoring_proportion)

        for headline in random.sample(headlines, max(self._num_headlines, len(headlines))):
            print headline
        won = False
        for i in xrange(self._guesses):
            guess = raw_input("> ")
            if guess.lower() == topic.lower():
                print "Yay!"
                won = True
                break
            else:
                print ":("
                continue

        return won

    def play(self, rounds):
        """
        Play a set number of rounds.

        :param rounds: The number of rounds
        :return: The number of rounds the user won (i.e. guessed the search term correctly)
        """
        won = 0
        for i in xrange(rounds):
            if self.new_round():
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
    won = g.play(rounds)
    print "{0}/{1} correct".format(won, rounds)
    raw_input()  # Keep from exiting immediately

if __name__ == "__main__":
    main()
