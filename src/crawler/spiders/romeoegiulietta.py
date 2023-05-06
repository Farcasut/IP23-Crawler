import scrapy
from itemloaders import ItemLoader
from ..items import Product
from scrapy.selector import Selector
from crawler import utils


class RomeoEGiulietta(scrapy.Spider):
    name = 'RomeoEGiulietta'
    start_urls = ['https://romeoegiuliettafood.com/livrare-la-domiciliu/']


    def parse(self, response):
        products_pages=  response.css('#apus-categories a::attr(href)').getall()
        for products_page in products_pages:
            if products_page != '/bucatarie-romaneasca/#target' and products_page != '/meniu-de-post-vegetarian/#target' :
                products_page = 'https://romeoegiuliettafood.com' + products_page
                yield response.follow(products_page, callback=self.scrape_page)

    def scrape_page(self, response):
        products = response.css('.food-menu-w2').getall()
        categorie = response.css('.w-divider6 h3 .spr::text').get()
        print(categorie)
        for product in products:
                yield self.scrape_item(product,categorie)

    def scrape_item(self, product, category):
        element = Selector(text=product)
        l = ItemLoader(item=Product(), selector=element)
        desc = element.css('.fm-w2-des::text').get()
        if desc == '.':
             desc = None
        desc = utils.get_rid_of_special_spaces(desc)
        l.add_value('restaurant_name', 'Romeo E Giulietta')
        l.add_value('name', utils.get_rid_of_slashes(element.css('.fm-w2-name::text').get().strip()))
        l.add_value('source', 'site')
        l.add_css('price', '.fm-w2-price::text')
        l.add_value('category', category)
        l.add_value('description', desc)
        return l.load_item()