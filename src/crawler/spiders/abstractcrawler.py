import scrapy
from scrapy.loader import ItemLoader
from abc import ABC, abstractmethod
from crawler.items import Product

class AbstractCrawler(ABC, scrapy.Spider):

    @property
    @abstractmethod
    def default_product_values(self) -> dict:
        pass
    
    @property
    @abstractmethod
    def product_selectors(self) -> dict:
        pass

    @property
    @abstractmethod
    def link_selectors(self) -> dict:
        pass
    
    @abstractmethod
    def parse(self, response):
        pass
    
    def helper_get_product(self, response, selector=None):
        item = ItemLoader(item=Product(), response=response, selector=selector)
        self.set_default_values_product(item)
        for key in self.product_selectors:
            item.add_css(key, self.product_selectors[key])
        
        return item.load_item()

    def set_default_values_product(self, item : ItemLoader):
        for key in self.default_product_values.keys():
            item.add_value(key, self.default_product_values[key])
