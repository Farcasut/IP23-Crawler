import scrapy

from itemloaders import ItemLoader
from ..items import Product
from crawler import utils

from scrapy import Selector

class BuenaVista(scrapy.Spider):
    name = 'BuenaVista'
    start_urls = [
        'https://www.buena-vista.ro/menu/'
    ]

    def parse(self, response):
        products = response.css(
            '.elementor-column.elementor-col-50 .elementor-column-wrap.elementor-element-populated .elementor-widget-wrap .elementor-element.sc_fly_static.elementor-widget.elementor-widget-text-editor .elementor-widget-container .elementor-text-editor.elementor-clearfix').getall()
        #print(products)
        for product in products:
            yield self.scrape_item(product)

    def scrape_item(self, product):
        element = Selector(text=product)
        desc = utils.get_rid_of_special_spaces_without_strip(element.css('.elementor-text-editor.elementor-clearfix p::text').get())
        desc = utils.check_existance(desc)
        nume = utils.get_rid_of_special_spaces(element.css('.menu_title h5::text').get())
        if nume != None :
            l = ItemLoader(item=Product(), selector=element)
            l.add_value('restaurant_name', BuenaVista.name)
            l.add_value('name', nume)
            l.add_value('source', 'site')
            l.add_css('price', '.menu_price::text')
            l.add_value('images', ' ')
            l.add_value('category', ' ')
            l.add_value('description', desc)
            return l.load_item()