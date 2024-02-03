from scraper import Scraper
from bs4 import BeautifulSoup
from tqdm import tqdm
from civitatis.data import Activity, Review
import itertools, re, urllib

class ActivityScraper(Scraper):
    
    def run(self, desc='Scraping urls'):
        # get first page
        html = super().request_with_cache(self.url, self.cache, self.headers)
        soup = BeautifulSoup(html, self.parser)
        pagination = soup.find_all('a', class_='paginationElement')
        urls = [self.url]+[page['data-href'] for page in pagination]        
        # get rest of pages
        items = []        
        for url in tqdm(urls, desc=desc):
            html = super().request_with_cache(url, self.cache, self.headers)
            soup = BeautifulSoup(html, self.parser)
            # get items
            item_list = soup.find_all('div', class_='o-search-list__item')
            items.append([Activity.scrape(item) for item in item_list])
            
        items = list(itertools.chain.from_iterable(items))
        self.items = [vars(item) for item in items]

class ReviewScraper(Scraper):
    
    def run(self, desc='Scraping urls'):
        # get first page        
        html = super().request_with_cache(self.url, self.cache, self.headers)
        soup = BeautifulSoup(html, self.parser)
        pagination = soup.find_all('a', {'title': re.compile(r'Opiniones - Página ')})
        urls = [self.url]+[urllib.parse.urljoin(self.get_homepage(), page['href']) for page in pagination]
        # get rest of pages
        items = []  
        for url in tqdm(urls, desc=desc):
            html = super().request_with_cache(url, self.cache, self.headers)
            soup = BeautifulSoup(html, self.parser)
            # get items
            item_list = soup.find_all('div', class_='o-container-opiniones-small')
            # exclude answers
            item_list = [item for item in item_list if '_answer' not in item.attrs['class']]
            items.append([Review.scrape(item, url) for item in item_list])
            
        items = list(itertools.chain.from_iterable(items))
        self.items = [vars(item) for item in items]