# gets rid of &nbsp;
def get_rid_of_special_spaces(element):
    if element is not None:
        return element.replace(u'\xa0', u' ').strip()
    else:
        return None

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
