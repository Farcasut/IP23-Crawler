from scrapy.crawler import CrawlerProcess

from crawler.settings import SETTINGS
from crawler.pipelines import CrawlerPipeline
from crawler.spiders.test import TestSpyder
from crawler.items import Quote
from crawler.pipelines import items

def main():
    process = CrawlerProcess(SETTINGS)

    process.crawl(TestSpyder)
    process.start()
    


if __name__ == '__main__':
    main()
