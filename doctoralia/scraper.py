from scraper import Scraper
from bs4 import BeautifulSoup
from doctoralia.data import Doctor
import itertools
from config import URL_SHORTENER

class DoctorScraper(Scraper):
    
    @classmethod
    def __get_items(cls, soup: BeautifulSoup):
        div = soup.find('div', {'id': 'search-content'})
        items_1 = div.findAll('li',{'class': 'has-cal-active'})
        items_2 = div.findAll('li',{'class': 'has-little-content'})
        items_3 = div.findAll('li',{'class': 'has-cal-commercial'})
        return items_1 + items_2 + items_3
        
    def run(self):
        # get first page
        html = super().request_with_cache(self.url, self.cache, self.headers)
        soup = BeautifulSoup(html, self.parser)
        item_list = DoctorScraper.__get_items(soup)
        new_items = [Doctor.scrape(item) for item in item_list]
        print(URL_SHORTENER.short(self.url), len(new_items))
        items = [new_items]
        # get next url
        a = soup.find('a', class_='page-link-next')
        while a is not None:
            next_url = a['href']
            html = super().request_with_cache(next_url, self.cache, self.headers)
            soup = BeautifulSoup(html, self.parser)
            item_list = DoctorScraper.__get_items(soup)
            new_items = [Doctor.scrape(item) for item in item_list]
            print(URL_SHORTENER.short(next_url), len(new_items))
            items.append(new_items)
            a = soup.find('a', class_='page-link-next')
        items = list(itertools.chain.from_iterable(items))
        self.items = [vars(item) for item in items]