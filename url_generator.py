import pandas as pd

class URL:
    def data(self):
        SEARCH_ENGINES = {
            "google": "https://www.google.com/search?q=",
            "youtube": "https://www.youtube.com/results?search_query=",
            "github": "https://github.com/search?q=",
            "stackoverflow": "https://stackoverflow.com/search?q=",
            "reddit": "https://www.reddit.com/search/?q=",
            "wikipedia": "https://en.wikipedia.org/w/index.php?search=",
            "duckduckgo": "https://duckduckgo.com/?q=",
            "bing": "https://www.bing.com/search?q=",
            "amazon": "https://www.amazon.com/s?k=",
            "ebay": "https://www.ebay.com/sch/i.html?_nkw=",
            "pypi": "https://pypi.org/search/?q=",
            "npm": "https://www.npmjs.com/search?q=",
            "mdn": "https://developer.mozilla.org/en-US/search?q=",
            "gfg": "https://www.geeksforgeeks.org/?s=",
            "w3schools": "https://www.w3schools.com/search/search.asp?search=",
            "medium": "https://medium.com/search?q=",
            "quora": "https://www.quora.com/search?q=",
            "imdb": "https://www.imdb.com/find?q="
            }
        return SEARCH_ENGINES
    def generate_base(self,engine):
        data=self.data()
        try:
            base=data[engine]
            return base
        except KeyError:
            return False
    def generate_query(self,engine,target):
        base=self.generate_base(engine)
        if not base:
            return False
        query=target.replace(" ","+")
        url=base+query
        return url
        
