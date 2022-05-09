import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

MYSQL_URI = os.environ['DATABASE_URI']
PREPROCESSOR = config['DEFAULT']['Preprocessor']
UPLOAD_FOLDER = config['DEFAULT']['UploadFolder']
ALLOWED_EXTENSIONS = config['DEFAULT']['AllowedExtensions'].split(",")
MAX_CONTENT_LENGTH = config['DEFAULT']['MaxContentLength']
CALORIE_NAME = config['Names']['calories']
FAT_NAME = config['Names']['fat']
CARBOHYDRATE_NAME = config['Names']['carbohydrate']
PROTEIN_NAME = config['Names']['protein']
