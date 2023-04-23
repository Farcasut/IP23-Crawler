from configparser import ConfigParser


#defines a config function to read the data form database.ini - DB info that we connect to
def config(filename='database.ini', section='postgresql'):
    #parser create
    parser = ConfigParser()
    parser.read(filename)

    db = {}

    if parser.has_section(section):
            param = parser.items(section)
            for param in param:
                db[param[0]] = param[1]

    else:
        raise Exception("Section {0} not found in the {1} file".format(section,filename))

    return db
