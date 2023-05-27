import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    p1 = multiprocessing.Process(target=task1)
    p1.start()
    p1.join()
    p2 = multiprocessing.Process(target=task2)
    p2.start()
    p2.join()
    p3 = multiprocessing.Process(target=task3)
    p3.start()
    p3.join()
    p4 = multiprocessing.Process(target=task4)
    p4.start()
    p4.join()
    p5 = multiprocessing.Process(target=task5)
    p5.start()
    p5.join()
    p6 = multiprocessing.Process(target=task6)
    p6.start()
    p6.join()
    p7 = multiprocessing.Process(target=images)
    p7.start()
    p7.join()

def task1():
    print("task1: starting")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl("PizzaSmile")
    process.crawl('CuptorulMoldovencei')
    process.crawl('SushiMaster')
    process.crawl('FireRibs')
    process.crawl('Veranda')

    process.start()
    print("task1: done")

def task2():
    print("task2: starting")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl('Krud')
    process.crawl('Odeon')
    process.crawl('Kraft')
    process.crawl('Bavaria')

    process.start()
    print("task2: done")

def task3():
    print("task3: starting")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl('Cheffa')
    process.crawl('Class')
    process.crawl('BlueAcqua')
    process.crawl('MoaraDeFoc')

    process.start()
    print("task3: done")

def task4():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    print("task4: starting")
    process.crawl('Rigatoni')
    process.crawl('Alila')
    process.crawl('BuenaVista')
    process.crawl('RomeoEGiulietta')
    process.crawl("MammaMia")
    process.start()
    print("task4: done")


def task5():
    print("task5: starting")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl('BerariaVeche')
    process.crawl('Vivo')
    process.crawl('CarulCuBurgeri')
    process.start()
    print("task5: done")

def task6():
    print("task6: starting")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl('Oscar')
    process.crawl('TikiBistro')
    process.crawl('Tazz')
    process.crawl('Glovo')
    process.start()
    print("task6: done")


def images():
    print("Downloading restaurant images")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl('RestaurantPhotos')
    process.start()
    


if __name__ == '__main__':
    main()
