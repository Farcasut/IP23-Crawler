import scrapy
from scrapy.loader import ItemLoader
from ..items import Product

class Veranda(scrapy.Spider):
    name = 'Veranda'
    start_urls = ['https://verandarestaurant.ro/']

    def parse(self, response):
        category_links = response.css('.menu-item-object-product_cat a::attr(href)').getall()
        category_names = response.css('.menu-item-object-product_cat a::text').getall()
        for pair in zip(category_links, category_names):
            yield response.follow(pair[0], callback=self.parse_category, cb_kwargs={'category': pair[1]})

    def parse_category(self, response, category):
        product_pages = response.css('.image a::attr(href)').getall()
        for product in product_pages:
            yield response.follow(product, callback=self.parse_product, cb_kwargs={'category': category})

    def parse_product(self, response, category):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', Veranda.name)
        l.add_value('source', 'site')
        l.add_value('category', category)
        l.add_css('name', '.heading-title::text')
        l.add_css('description', '.woocommerce-product-details__short-description p::text')
        l.add_css('price', 'bdi::text')
        l.add_css('images', '.wp-post-image::attr(src)')

        yield l.load_item()
