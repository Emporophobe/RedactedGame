from Censor import *
import random


class Game:
    _topic_list = []
    _random_censoring_proportion = 0
    _num_headlines = 0
    _guesses = 0
    _censor = Censor()

    def __init__(self, topics_file, random_censoring=0.1, num_headlines=10, guesses=1):
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
        won = 0
        for i in xrange(rounds):
            if self.new_round():
                won += 1
        print "{0}/{1} correct".format(won, rounds)
        raw_input()  # Keep from exiting immediately

if __name__ == "__main__":
    g = Game("topics.txt")
    g.play(5)
