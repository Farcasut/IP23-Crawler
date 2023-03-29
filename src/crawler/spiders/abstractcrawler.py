import scrapy
from scrapy.loader import ItemLoader
from abc import ABC, abstractmethod
from crawler.items import Product

class AbstractCrawler(ABC, scrapy.Spider):
    
    @abstractmethod
    def __init__(self, selectors : dict):
        self.css_selectors = selectors

    def parse(self, response : scrapy.http.HtmlResponse):
        item = ItemLoader(item=Product(), response=response)
        
        for key in dict(self.css_selectors).keys():
                item.add_css(key, self.css_selectors[key])

        yield item.load_item()
