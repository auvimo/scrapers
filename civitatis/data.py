from data import Item
from bs4 import Tag
import unicodedata

class Activity(Item):
    
    @classmethod
    def scrape(cls, item: Tag):
        res = {}
        try:          
            res['url'] = item.find('a', class_='_activity-link')['href']
            res['title'] = item.find('h3', class_='comfort-card__title').text.strip()
            res['rating'] = item.find('span', class_='m-rating--text')
            if res['rating']:
                res['rating'] = float(res['rating'].find(string=True, recursive=False).strip().replace(',', '.'))   
            res['review_count'] = cls._Item__get_int_value(item, 'span', 'text--rating-total', default_value=0)
            res['traveler_count'] = cls._Item__get_int_value(item, 'span', 'comfort-card__traveler-count _full', default_value=0)
            res['destination'] = item.find('span', class_='__city')
            if res['destination']:
                res['destination'] = res['destination'].text.strip()
            res['cancelation'] = item.find('div', class_='comfort-card__cancelation')
            if res['cancelation']:
                res['cancelation'] = res['cancelation'].text.strip()       
            unicode_str = item.find('div', class_='comfort-card__text').text.strip()
            res['description'] = unicodedata.normalize('NFKD', unicode_str)
            res['duration'] = item.find('span', class_='_duration')
            if res['duration']:
                res['duration'] = res['duration'].text.strip()
            res['language'] = item.find('span', class_='_lang')
            if res['language']:
                res['language'] = res['language'].text.strip()
            res['target'] = item.find('span', class_='_new-list-feature')
            if res['target']:
                res['target'] = res['target'].text.strip()
            res['price'] = item.find('span', class_='comfort-card__price__text').text.strip()
            res['html'] = str(item)
        except Exception as e:
            print(str(item))
            raise e            
        return Activity(res)

class Review(Item):
    
    @classmethod
    def scrape(cls, item: Tag, activity_path: str):
        res = {}
        try:        
            res['rating'] = item.find('span', class_='m-rating__stars__full').text.strip()
            res['date'] = item.find('p', class_='a-opiniones-date').text.strip().replace(' ', '')
            res['name'] = item.find(['div', 'span'], class_='opi-name').text.strip()
            res['location'] = item.find('p', class_='opi-location').text.strip()
            res['type'] = item.find('div', class_='a-opiniones-type').text.strip()
            unicode_str = item.find('div', class_='container-opinion-txt').text.strip()
            res['opinion'] = unicodedata.normalize('NFKD', unicode_str)
            res['url'] = activity_path
            res['html'] = str(item)                
        except Exception as e:
            print(str(item))
            raise e
        return Review(res)