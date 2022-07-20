DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'coilclean'
DB_HOST = 'localhost:3306'

FLASK_DEBUG = True
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@'+DB_HOST+'/' + DB_NAME
SQLALCHEMY_DATABASE_URI = 'sqlite:///./coil_db.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 300
SECRET_KEY = "dfhgfhdjghfdghufdhguifhuitrheui78476375646876uergfjhdsgfh"
