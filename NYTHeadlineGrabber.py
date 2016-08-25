import urllib2
import json


class NYTHeadlineGrabber:
    """
    Handle API calls to the New York Times website.
    """
    api_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    parsed = ""

    def __init__(self):
        return

    def get_json(self, search):
        """
        Get the json returned by the NYT API.

        :param search: The search query
        :return: A json-formatted string containing the articles about the search
        """
        return urllib2.urlopen(self.api_url + "?q=" + search).read()

    def parse_headlines(self):
        """
        Parse json string and get a list of the headlines in it.

        :return: A list of headline strings
        """
        headlines = []
        for headline in self.parsed["response"]["docs"]:
            headlines.append(headline["headline"]["main"])

        return headlines

    def get_headlines(self, search):
        """
        Create a list of headlines relating to the search query.

        :param search: The search query
        :return: A list of strings, each string is a headline of an article about the search
        """
        self.parsed = json.loads(self.get_json(search))
        return self.parse_headlines()
