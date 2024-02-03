from cache import Cache
import requests, urllib
import pandas as pd

class Scraper():
    """Automated tool to extract data from website"""
    
    def __init__(self, url, cache, headers, parser):
        self.url = url
        self.cache = cache
        self.headers = headers
        self.parser = parser
    
    @classmethod
    def request_with_cache(cls, url: str, cache: Cache, headers: dict, print_url: bool=False):
        """Fetch content from a URL"""
        # check if the response is already cached
        cached_data = cache.get(url)
        if cached_data:
            if print_url:
                print(f"Using cached data for {url}")
            return cached_data#, url

        # if not cached, send an HTTP request
        response = requests.get(url, headers=headers)
        if print_url:
            print(f"Cache not found for {url}")

        if response.status_code == 200:
            # cache the response for future use
            cache.set(url, response.text)
            return response.text#, response.url
    
    def get_data(self):
        return pd.DataFrame(self.items)
    
    def get_homepage(self):
        return urllib.parse.urljoin(self.url, '/')