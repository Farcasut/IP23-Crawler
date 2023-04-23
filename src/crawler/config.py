from configparser import ConfigParser

#You will need to create a database.ini file which will have:
#host=
#user=
#database =
#password=

#The paramaters will need to be provided by the devOPS team, you need to ask for it.

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
