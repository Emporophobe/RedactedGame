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
            for headline_word in headline.split():
                if any(map(lambda search_word: search_word.lower() in headline_word.lower(), term.split()))\
                        or (len(headline_word) > 2 and random.random() < random_censoring):
                    new_headline.append(self.censor_char * len(headline_word))
                else:
                    new_headline.append(headline_word)
                    
            censored.append(" ".join(new_headline))

        return censored
