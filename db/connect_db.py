import pathlib

import certifi
from mongoengine import connect
import configparser

default_values = {
    "USER": "user",
    "PASSWORD": "password",
    "DB_DOMAIN": "goit-python-web.2s0nqns.mongodb.net",
    "DB_NAME": "db",
}

config_path = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser(default_values)
config.read(config_path)


mongo_user = config.get("DB", "USER")
mongodb_pass = config.get("DB", "PASSWORD")
domain = config.get("DB", "DB_DOMAIN")
db_name = config.get("DB", "DB_NAME")

uri = f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"""

connect(host=uri, tlsCAFile=certifi.where(), ssl=True)
