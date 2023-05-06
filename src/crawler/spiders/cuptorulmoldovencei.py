import scrapy
from itemloaders import ItemLoader

from crawler import utils
from ..items import Product


class CuptorulMoldovencei(scrapy.Spider):
    name = 'CuptorulMoldovencei'
    start_urls = [
        'https://cuptorulmoldovencei.ro/shop-online/'
    ]

    def parse(self, response):
        product_pages = response.css(
            '.woocommerce-LoopProduct-link.woocommerce-loop-product__link::attr(href)').getall()
        for product_page in product_pages:
            yield response.follow(product_page, callback=self.scrape_item)

    def scrape_item(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', 'Cuptorul Moldovencei')
        l.add_css('name', '.entry-title::text')
        l.add_value('source', 'site')
        l.add_value('price', utils.get_rid_of_special_spaces(
            response.css('.elementor-widget-woocommerce-product-price bdi::text').get()))
        l.add_css('images', '.size-2048x2048::attr(src)')
        l.add_value('category', "pastry /bakery")
        l.add_value('description', "\n".join(response.css('p::text').getall()))
        yield l.load_item()
