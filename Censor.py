from NYTHeadlineGrabber import *
import random


class Censor:
    headline_handler = NYTHeadlineGrabber()
    censor_char = u"\u2588"  # solid black box

    def __init__(self):
        return

    def create_censored_headlines(self, term, random_censoring=0.1):
        original = self.headline_handler.get_headlines(term)
        censored = []
        for headline in original:
            new_headline = []
            for word in headline.split():
                # Randomly select additional words to censor in addition to the key word
                if term in word\
                        or (random.random() < random_censoring and len(word) > 2):
                    new_headline.append(self.censor_char * len(word))
                else:
                    new_headline.append(word)
            censored.append(" ".join(new_headline))

        return censored
