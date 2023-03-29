import scrapy
from scrapy.loader import ItemLoader
from crawler.items import Product
from crawler.items import Quote

class TestSpyder(scrapy.Spider):
    name = 'test'
    start_urls = ["https://quotes.toscrape.com"]
    
    def __init__(self):
        self.crawled_items = []

    def parse(self, response : scrapy.http.HtmlResponse):
        item = ItemLoader(item=Quote(), response=response)
        item.add_css('product_name', "div[class='col-md-8'] div:nth-child(2) span:nth-child(1)")    

        yield item.load_item()
