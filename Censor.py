from NYTHeadlineGrabber import *
import random


class Censor:
    """
    Sensor headlines based on the search term and optionally censor random additional words.
    """
    headline_handler = NYTHeadlineGrabber()
    censor_char = u"\u2588"  # solid box

    def __init__(self):
        return

    def create_censored_headlines(self, term, random_censoring=0):
        """
        Create a list of censored headline strings.

        :param term: The search term for which to find news headlines.
        :param random_censoring: The proportion [0, 1] of words to randomly censor .
        :return: A list of strings, each string being a headline with portions replaced with a unicode box.
        """
        original = self.headline_handler.get_headlines(term)
        censored = []
        for headline in original:
            new_headline = []
            for word in headline.split():
                # Randomly select additional words to censor in addition to the key word
                if term.lower() in word.lower()\
                        or (random.random() < random_censoring and len(word) > 2):  # len > 2 so words like "a" are ok
                    new_headline.append(self.censor_char * len(word))
                else:
                    new_headline.append(word)
            censored.append(" ".join(new_headline))

        return censored
