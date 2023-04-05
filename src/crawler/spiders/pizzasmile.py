import scrapy
from itemloaders import ItemLoader

from crawler.items import Product

class PizzaSmile(scrapy.Spider):
    name = 'PizzaSmile'
    start_urls = [
        'https://smilepizzadelivery.ro/delivery/'
    ]

    def parse(self, response):
        product_pages = response.css('.woocommerce-loop-product__link::attr(href)').extract()
        next_page = response.css('.next::attr(href)').get()

        for product_page in product_pages:
            yield response.follow(product_page, callback=self.scrapeItem)

        if next_page is not None:
            print("\n\n\n\n\n\n" + next_page + "n\n\n\n\n\n\n")
            yield response.follow(next_page, self.parse)

    def scrapeItem(self, response):
        l = ItemLoader(item=Product(), selector=response)
        l.add_value('restaurant_name', PizzaSmile.name)
        l.add_css('name', '.edgtf-single-product-title::text')
        l.add_value('source', 'site')
        l.add_css('price', '.entry-summary .amount::text')
        l.add_css('images', '.wp-post-image::attr(src)')
        l.add_css('category', '.edgtf-woo-cat-items a::text')
        l.add_css('description', 'strong::text')
        yield l.load_item()


