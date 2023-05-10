import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product
class MoaraDeFoc(scrapy.Spider):
    name = 'MoaraDeFoc'
    start_urls = ['https://moaradefoc.ro/livrari-domiciliu/preparate/']
    def parse(self, response):
        products = response.css('.tmb-woocommerce .pushed::attr(href)').getall()
        for product_page in products:
            yield response.follow(product_page, callback=self.scrape_item)


    def scrape_item(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', 'Moara de Foc')
        l.add_css('name', '.entry-title::text')
        l.add_value('source', 'site')
        l.add_css('price', '.price-container .amount::text'),
        l.add_css('images', '.attachment-full.size-full.wp-post-image::attr(src)')
        l.add_value('category', '')
        l.add_css('description', 'p:nth-child(2)::text')
        yield l.load_item()
