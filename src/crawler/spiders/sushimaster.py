import scrapy
from itemloaders import ItemLoader

from crawler.items import Product


class SushiMaster(scrapy.Spider):
    name = 'SushiMaster'
    start_urls = [
        'https://sushimaster.ro/'
    ]

    def parse(self, response):
        pages_id = response.css('.production-card::attr(data-category-id)').getall()
        category = response.css('h2::text').getall()
        for pair in zip(pages_id, category):
            yield response.follow(SushiMaster.start_urls[0] + 'menu/' + pair[0], callback=self.scrape_page,
                                  cb_kwargs={'category': pair[1]})

    def scrape_page(self, response, category):
        prices = response.css('.price::text').getall()
        names = response.css('h4::text').getall()
        descriptions = response.css('p::text').getall()
        images = response.css('.available img::attr(src)').getall()

        for i in zip(names, descriptions, prices, images):
            l = ItemLoader(item=Product(), selector=response)
            l.add_value('restaurant_name', SushiMaster.name)
            l.add_value('source', 'site')
            l.add_value('category', category)
            l.add_value('name', i[0].strip())
            l.add_value('description', i[1])
            l.add_value('price', i[2].strip())
            l.add_value('images', i[3])
            yield l.load_item()
