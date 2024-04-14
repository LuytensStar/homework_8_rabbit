from mongoengine import connect
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongo_password = config.get('DB', 'pass')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'domain')

connect(host = f"""mongodb+srv://{mongo_user}:{mongo_password}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl = True)

