from scraper import Scraper
from bs4 import BeautifulSoup
from tqdm import tqdm
from visiondirect.data import Product, Review
import itertools, re, urllib, json

class ProductScraper(Scraper):
    
    def run(self, desc='Scraping urls'):
        # without pagination on brand product-listing
        html = super().request_with_cache(self.url, self.cache, self.headers)
        soup = BeautifulSoup(html, self.parser)
        # get items
        item_list = soup.find_all('a', class_='products-list__item')
        items = [] 
        for item in tqdm(item_list, desc=desc):
            url = item['href']
            html = super().request_with_cache(url, self.cache, self.headers)
            soup = BeautifulSoup(html, self.parser)
            # check product status
            discontinued = re.search('"product_status"\:"discontinued"', html, re.IGNORECASE)
            if not discontinued:
                items.append(Product.scrape(soup.find('ul', class_='product-page'), url))
        self.items = [vars(item) for item in items]

class ReviewScraper(Scraper):
    
    def run(self, url, desc='Scraping urls'):
        # without pagination on product review-listing       
        json_str = super().request_with_cache(self.url, self.cache, self.headers)
        # convert string to dict
        item_list = json.loads(json_str)['items']
        items = []
        for item in tqdm(item_list, desc=desc):
            items.append(Review.scrape(BeautifulSoup(item, self.parser), url))
        self.items = [vars(item) for item in items]