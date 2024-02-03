from bs4 import Tag
import re

class Item():
    
    # https://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python
    def __init__(self, *initial_data, **kwargs):
        
        for key in kwargs:
            setattr(self, key, kwargs[key])
            
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
            
    def __str__ (self):
        return str(self.__dict__)
    
    @classmethod
    def __get_int_value(cls, item: Tag, html_tag: str, class_attr: str, default_value=None):
        item = item.find(html_tag, class_=class_attr)
        value = default_value
        if item:
            m = re.search('(\d+(?:.\d+)?)', item.text.strip())
            if m:
                value = int(m.group(1).replace('.', ''))
        return value
    
    @classmethod
    def __get_float_value(cls, item: Tag, html_tag: str, class_attr: str, default_value=None):
        item = item.find(html_tag, class_=class_attr)
        value = default_value
        if item:
            m = re.search('(\d+(?:,\d+)?)', item.text.strip())
            if m:
                value = float(m.group(1).replace(',', '.'))
        return value    
    
    @classmethod
    def scrape(cls):
        raise NotImplementedError("Don't forget to implement the scrape method")