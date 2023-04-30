from scrapy import Request

# gets rid of &nbsp;
def get_rid_of_special_spaces(element):
    if element is not None:
        return element.replace(u'\xa0', u' ').strip()
    else:
        return None

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
def create_selenium_driver():
    options = Options()
    options.add_argument('-headless')
    driver = WebDriver(options=options)
    return driver


class SeleniumRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(self, wait_time=None, wait_until=None, screenshot=False, script=None, *args, **kwargs):
        """Initialize a new selenium request

        Parameters
        ----------
        wait_time: int
            The number of seconds to wait.
        wait_until: method
            One of the "selenium.webdriver.support.expected_conditions". The response
            will be returned until the given condition is fulfilled.
        screenshot: bool
            If True, a screenshot of the page will be taken and the data of the screenshot
            will be returned in the response "meta" attribute.
        script: str
            JavaScript code to execute.

        """

        self.wait_time = wait_time
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script = script

        super().__init__(*args, **kwargs)

from configparser import ConfigParser
def parse_config(filename='crawler/configs/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    database_configuration = {}

    if parser.has_section(section):
        parameters = parser.items(section)
        for parameter in parameters:
            database_configuration[parameter[0]] = parameter[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file.")

    return database_configuration

import psycopg2
def create_db_connection():
    db_connection = None
    try:
        db_configuration = parse_config()
        db_connection = psycopg2.connect(**db_configuration)

    except (Exception, psycopg2.DataError) as error:
        print(f"There was an error: {error}")
   
    return db_connection 

def get_rid_of_special_spaces_without_strip(element):
    if element is not None:
        return element.replace(u'\xa0', u' ')
    else:
        return None

def check_existance(element):
    if element is None:
        return(' ')
    else:
        return element

    