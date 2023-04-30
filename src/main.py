from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



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
    process.crawl('Rigatoni')
    process.crawl('BerariaVeche')
    process.crawl('Cheffa')
    process.crawl('Vivo')
    process.crawl('Class')
    process.crawl('Glovo')
    process.crawl('Alila')
    process.crawl('BuenaVista')
    process.start()
    


if __name__ == '__main__':
    main()