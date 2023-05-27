import re
import scrapy
from itemloaders import ItemLoader
from scrapy import Selector
from ..items import Product


class Oscar(scrapy.Spider):
    name = 'Oscar'
    start_urls = ['https://restaurant-oscar.ro/']

    def parse(self, response):
        categories_pages = response.css('.wp-block-kadence-column .wp-block-kadence-infobox .kt-blocks-info-box-link-wrap::attr(href)').getall()
        for category_page in categories_pages:
            yield response.follow(category_page, callback= self.scrape_page)

    def scrape_page(self, response):
        products = response.css('.woocommerce-loop-product__title a::attr(href)').getall()
        for product in products:
            yield response.follow(product, callback=self.scrape_item)

    def scrape_item(self, response,):
        l = ItemLoader(item = Product(), selector= response)
        l.add_value('restaurant_name',Oscar.name)
        l.add_value('delivery_price', '15')
        l.add_value('min_delivery', '50')
        l.add_css('name', '.entry-title::text')
        l.add_value('source', 'site')
        l.add_css('price', '.price bdi::text')
        l.add_css('images', '.product_image a::attr(href)')
        l.add_css('category', '.single-product-category a::text')
        l.add_css('description', '#tab-description p::text')
        yield l.load_item()