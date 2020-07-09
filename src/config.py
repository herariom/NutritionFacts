import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TESSERACT_PATH = config['DEFAULT']['TesseractPath']
MYSQL_URI = config['DEFAULT']['DatabaseURI']
PREPROCESSOR = config['DEFAULT']['Preprocessor']
UPLOAD_FOLDER = config['DEFAULT']['UploadFolder']
ALLOWED_EXTENSIONS = config['DEFAULT']['AllowedExtensions'].split(",")
