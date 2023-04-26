import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product
class kraft(scrapy.Spider):
    name = 'Kraft'
    start_urls = ['https://kraftpub2.com/index.php?dispatch=products.search&search_performed=Y']
    def parse(self, response):
        products_pages = response.css('.product-title::attr(href)').getall()
        next_page =  response.css('.ty-pagination__items a::attr(href)').get();
        for product_page in products_pages:
            yield response.follow(product_page, callback=self.scrape_item)
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def scrape_item(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', kraft.name)
        l.add_css('name', '#et_prod_title bdi::text')
        l.add_css('source', 'site')
        l.add_value('price', response.css('.ty-price-num::text').get()),
        l.add_value('images',  response.css('#et-product-page .cm-image::attr(src)').get())
        l.add_value('category', '')
        l.add_value('description', '')
        yield l.load_item()