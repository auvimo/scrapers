from data import Item
from bs4 import Tag

class Doctor(Item):
    
    @classmethod
    def scrape(cls, item: Tag):
        res = {}
        try:
            res['doctor_id'] = item.find('div')['data-eecommerce-id']
            res['name'] = item.find('div')['data-doctor-name']
            res['url'] = item.find('div')['data-doctor-url']
            res['speciality'] = item.find('div')['data-eecommerce-category']
            a = item.find('a', {'data-tracking-id':'result-card-reviews'})
            if a:
                res['rating'] = float(a.find('span', {'class':'rating'})['data-score'])
                res['review_count'] = cls._Item__get_int_value(item, 'span', 'opinion-numeral', default_value=0)
            else:
                res['rating'] = None
                res['review_count'] = 0     
            try:
                address_data = item.find('div', {'data-id':'result-address-item'})
                res['address_lat'] = address_data['data-lat']
                res['address_lng'] = address_data['data-lng']            
            except:
                res['address_lat'] = None
                res['address_lng'] = None
            res['html'] = str(item)
        except Exception as e:
            print(str(item))
            raise e            
        return Doctor(res)