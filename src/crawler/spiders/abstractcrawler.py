import scrapy
from scrapy.loader import ItemLoader
from abc import ABC, abstractmethod
from crawler.items import Product

class AbstractCrawler(ABC, scrapy.Spider):
    """
        The derived classes of the abstract class **must** contain
        the dict()s type fileds in the body of the class, those are:
            * default_product_value = {}
            * product_selectors = {}
            * link_selectors = {}

        IMPORTANT: The KEYS of the dictonaries **default_product_values**
        and **product_selectors** must be set as str() of the name of the
        fields from the Product class so that the union between
        default_product_values.keys() + product_selectors.keys() = Product.fields
 
    """

    """
        The **default_product_values** dictonary it can be set so that if
        the website does not contain the information required it can
        be set by a specified placeholder
    """
    @property
    @abstractmethod
    def default_product_values(self) -> dict:
        pass
    
    """
        The **product_selectors** it uses CSS selector to select the
        information required from a response from a site and fill the
        Product item object. 
    """
    @property
    @abstractmethod
    def product_selectors(self) -> dict:
        pass

    """
        TODO: The **link_selector** specifies the CSS selectors to be used
        for browsing the next page required by the user.
    """
    @property
    @abstractmethod
    def link_selectors(self) -> dict:
        pass
    
    """
        Method created by scrapy.Spide which is optional
        In case is not created the derived crawler will start the scrapy.Request
        for each url from start_urls = [] list.
    """
    def start_requests(self):
        pass

    """
        Method created by scrapy.Spider which must be implemented
    """
    @abstractmethod
    def parse(self, response):
        pass

    """
        This helper function takes a response and a selector (which is optional)
        The selector will be set if there are more products in a page that are
        needed to be parsed else the first product will be parsed.
        Example with selector=None when the crawled page has only one product.
    """
    def helper_get_product(self, response, selector=None):
        item = ItemLoader(item=Product(), response=response, selector=selector)
        self.set_default_values_product(item)
        for key in self.product_selectors:
            item.add_css(key, self.product_selectors[key])
        
        return item.load_item()

    def set_default_values_product(self, item : ItemLoader):
        for key in self.default_product_values.keys():
            item.add_value(key, self.default_product_values[key])
