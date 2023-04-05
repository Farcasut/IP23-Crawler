import scrapy
from crawler.spiders.abstractcrawler import  AbstractCrawler


class PizzaSmile(AbstractCrawler):


    name = 'PizzaSmile'
    start_urls = [
        'https://smilepizzadelivery.ro/delivery/'
    ]
    link_selectors={'.next::attr(href)'}
    product_selectors = {"product_name" : ".woocommerce-loop-product__link::attr(href)",
                         "product_description" : "strong::text",
                         "product_price" : '.entry-summary .amount::text',
                         'product_images' : '.wp-post-image::attr(data-.src)'
                         }
    default_product_values = {"restaurant_name" : "PizzaSmile", "source" : "site", "product_category" : "generic_category"}


    def parse(self, response):
        product_pages = response.css('.woocommerce-loop-product__link::attr(href)').extract()
        for product_page in product_pages:
            yield self.helper_get_product(response=response, selector=product_page)


