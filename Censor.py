from NYTHeadlineGrabber import *
import random


class Censor:
    headline_handler = NYTHeadlineGrabber()
    censor_text = "*****"

    def __init__(self):
        return

    def create_censored_headlines(self, term, randomcensoring=0.1):
        original = self.headline_handler.get_headlines(term)
        censored = []
        for headline in original:
            # TODO: replace with regex or something more robust
            censored.append(headline.replace(term, self.censor_text))

        censored = self.random_censoring(censored, randomcensoring)

        return censored

    def random_censoring(self, headlines, proportion=0.1):
        scrambled = []
        for headline in headlines:
            new_headline = ""
            for word in headline.split():
                if random.random() < proportion:
                    new_headline += " " + self.censor_text + " "
                else:
                    new_headline += " " + word + " "
            scrambled.append(new_headline)
        return scrambled

if __name__ == "__main__":
    c = Censor()
    scrubbed = c.create_censored_headlines("Trump")

    for h in scrubbed:
        print h
