import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    HOST = os.getenv('DB_HOST', "localhost")
    DATABASE = os.getenv('DB_DATABASE', "belajar_migrasi")
    USERNAME = os.getenv('DB_USERNAME', "root")
    PASSWORD = os.getenv('DB_PASSWORD', "")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_RECORD_QUERIES = True