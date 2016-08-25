import urllib2
import json


class NYTHeadlineGrabber:

    api_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    parsed = ""

    def __init__(self):
        return

    def get_json(self, search):
        return urllib2.urlopen(self.api_url + "?q=" + search).read()

    def parse_headlines(self):
        headlines = []
        for headline in self.parsed["response"]["docs"]:
            headlines.append(headline["headline"]["main"])

        return headlines

    def get_headlines(self, search):
        self.parsed = json.loads(self.get_json(search))
        return self.parse_headlines()


if __name__ == "__main__":
    hg = NYTHeadlineGrabber()
    for h in hg.get_headlines("trudeau"):
        print h
