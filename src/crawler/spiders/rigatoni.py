import re
import scrapy
from itemloaders import ItemLoader
from ..items import Product

class Rigatoni(scrapy.Spider):
    name = 'Rigatoni'
    start_urls = ['https://rigatoni.ro/iasi/']


    def parse(self, response):
        products_pages=  response.css('.menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children.menu-item-4617 ul .menu-item.menu-item-type-taxonomy a::attr(href)').getall()[:4]
        for products_page in products_pages:
            yield response.follow(products_page, callback=self.scrape_page)


    def scrape_page(self, response):
        products = response.css('.image a::attr(href)').getall()
        for prodcut in products:
            yield response.follow(prodcut, callback=self.scrape_item)
    def scrape_item(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', Rigatoni.name)
        l.add_value('delivery_price', '15')
        l.add_value('min_delivery', '0')
        l.add_css('name', '.heading-title::text')
        l.add_value('source', 'site')
        l.add_css('price', 'bdi::text')

        l.add_css('images', '.wp-post-image::attr(src)')
        l.add_css('category', '.product_meta a::text')
        l.add_css('description', '.woocommerce-product-details__short-description p::text')
        yield l.load_item()
