import scrapy
from scrapy.loader import ItemLoader

from ..items import Product
class ManPizza(scrapy.Spider):
    name = 'Man Pizza'
    start_urls = ['https://www.manpizza.ro']


    def parse(self, response):
        category_links = response.css('#left-menu li a::attr(href)').getall()
        category_names = response.css('#left-menu li a::text').getall()
        for pair in zip(category_links, category_names):
            yield response.follow(pair[0], callback=self.parse_category, cb_kwargs={'category':pair[1]})


    def parse_category(self, response, category):
        product_pages = response.css('.product_info a::attr(href)').getall()
        for product in product_pages:
            yield response.follow(product, callback=self.parse_product, cb_kwargs={'category':category})


    def parse_product(self, response, category):
        l = ItemLoader(item = Product(), selector= response)
        l.add_value('restaurant_name', ManPizza.name)
        l.add_value('delivery_price', '0')
        l.add_value('min_delivery', '50')
        l.add_value('source', 'site')
        l.add_value('category', category)
        l.add_css('name', '.product_info .description .underline2 a::text')
        l.add_css('description', '.product_info .description  p::text')
        l.add_css('images', '.product-info img::attr(src)')
        l.add_css('price', '.product_info .price::text')

        yield  l.load_item()



