import scrapy
from itemloaders import ItemLoader


from crawler.items import Product
from crawler.spiders import utils


class PizzaSmile(scrapy.Spider):
    name = 'PizzaSmile'
    start_urls = [
        'https://smilepizzadelivery.ro/delivery/'
    ]

    def parse(self, response):
        product_pages = response.css('.woocommerce-loop-product__link::attr(href)').getall()
        next_page = response.css('.next::attr(href)').get()

        for product_page in product_pages:
            yield response.follow(product_page, callback=self.scrape_item)

        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def scrape_item(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', PizzaSmile.name)
        l.add_css('name', '.edgtf-single-product-title::text')
        l.add_value('source', 'site')
        l.add_value('price', utils.get_rid_of_special_spaces(response.css('.entry-summary .amount::text').get())),
        l.add_css('images', '.wp-post-image::attr(src)')
        l.add_css('category', '.edgtf-woo-cat-items a::text')
        l.add_value('description', utils.get_rid_of_special_spaces(response.css('strong::text').get()))
        yield l.load_item()


