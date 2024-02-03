from data import Item
from bs4 import Tag
import re

class Product(Item):
    
    @classmethod
    def scrape(cls, item: Tag, url: str):
        res = {}
        try:          
            res['url'] = url
            res['name'] = item.find('h1', itemprop='name').text.strip()
            reviewContainer = item.find(id='reviewContainer')
            res['product_id'] = None
            res['review_count'] = None           
            if reviewContainer:
                res['product_id'] = reviewContainer['data-productid']
                res['review_count'] = reviewContainer['data-totalnumber']
            res['deal_price'] = cls._Item__get_float_value(item, 'span', 'price ours')
            res['price'] = cls._Item__get_float_value(item, 'span', 'price theirs price--hs')            
            res['html'] = str(item)
        except Exception as e:
            print(str(item))
            raise e            
        return Product(res)

class Review(Item):
    
    @classmethod
    def scrape(cls, item: Tag, url: str):
        res = {}
        try:          
            res['url'] = url
            created_at = item.find('span', class_='review-createdat').text
            res['created_at'] = re.search('\(Realizada (.*)\)', created_at, re.IGNORECASE).group(1)
            res['opinion'] = item.find("span", class_="review-detail").text.strip()
            star_rating = item.find_all("span", class_="star-rating__gold review-rating-star")
            if len(star_rating) == 3:
                [res['comfort'], res['quality_price_ratio'], res['vision']] = [int(re.findall(r'\d+', rate["style"])[0]) for rate in star_rating]
            res['html'] = str(item)
        except Exception as e:
            print(str(item))
            raise e            
        return Review(res)