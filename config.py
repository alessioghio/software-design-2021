class Config:
    # Set Flask config variables
    SECRET_KEY = "software-design-2021"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/productsImages'
    UPLOAD_FOLDER2 = 'static/recipesImages'

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    TEMPLATES_AUTO_RELOAD = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True