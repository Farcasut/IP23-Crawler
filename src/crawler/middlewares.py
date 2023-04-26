from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from crawler.utils import SeleniumRequest

"""
    Creates a middleware that can be used with SeleniumRequest.
    If you want to use the middleware the class must have the field ``driver``
    initilized to a selenium driver else on the first call on SeleniumRequest the
    driver will be added to the spider object and it can be later used in the program, 
    the driver will be unique to each spider.

    This class will also autoclose the driver from the spider.
"""
class SeleniumMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        if isinstance(request, SeleniumRequest):
            if not hasattr(spider, 'driver'):
                self.create_driver(spider)
            driver = spider.driver

            for cookie_name, cookie_value in request.cookies.items():
                driver.add_cookie(
                    {
                        'name': cookie_name,
                        'value': cookie_value
                    }
                )

            if request.wait_until:
                WebDriverWait(driver, request.wait_time).until(
                    request.wait_until
                )

            if request.screenshot:
                request.meta['screenshot'] = driver.get_screenshot_as_png()

            if request.script:
                driver.execute_script(request.script)

            driver.get(request.url)
            body = driver.page_source
            return HtmlResponse(url=driver.current_url, body=body, encoding='utf-8')

    def create_driver(self, spider):
        options = Options()
        options.add_argument('-headless')
        driver = WebDriver(options=options)
        spider.driver = driver

    def spider_closed(self, spider):
        driver = getattr(spider, 'driver', None)
        if driver:
            driver.quit()
