from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # creating parser
    parser = ConfigParser()
    # read file
    parser.read(filename)

    # getting section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception()
    return db


config()
