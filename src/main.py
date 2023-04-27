from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawler.pipelines import CrawlerPipeline
from crawler.pipelines import items

def main():
    settings = get_project_settings()
    print(settings)
    process = CrawlerProcess(settings)
    process.crawl("MammaMia")
    process.crawl("PizzaSmile")
    process.crawl('CuptorulMoldovencei')
    process.crawl('Tazz')
    process.crawl('SushiMaster')
    process.crawl('FireRibs')
    process.crawl('Veranda')
    process.crawl('Krud')
    process.crawl('Odeon')
    process.crawl('Kraft')
    process.crawl('Bavaria')
    process.crawl('Cheffa')
    process.crawl('BerariaVeche')
    process.start()
    print(items)


if __name__ == '__main__':
    main()