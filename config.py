import os




class Config(object):
    UPLOAD_FOLDER = "/temporary"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_STRING")

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    # MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    APP_STATE = os.environ.get("APP_STATE")  # production, development, debug, shutdown

    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_SECRET")
    RECAPTCHA_PUBLIC_KEY = "6LfFdWkUAAAAALQkac4_BJhv7W9Q3v11kDH62aO2"
    RECAPTCHA_PARAMETERS = {"hl": "cs", "render": "explicit"}

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    PASSWORD_VERSION = os.environ.get("PASSWORD_VERSION")

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    STORAGE_SYSTEM = os.environ.get("STORAGE_SYSTEM")  # DEFAULT, AWS

    BUCKET = "ketocalc"

    SENTRY_MONITORING = True
    INFO_USED_DB = "production db"



class LocalProdConfig(Config):
    INFO_USED_DB = "production db"
    TEMPLATES_AUTO_RELOAD = True


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_DB_STRING")
    SECRET_KEY = os.environ.get("TESTING_SECRET_KEY")
    SENTRY_MONITORING = False


class DevConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("LOCAL_DB_STRING")
    SENTRY_MONITORING = False
    BUCKET = "ketocalcdev"

    INFO_USED_DB = "local db"

    DEV_PASSWORD = os.getenv("DEV_PASSWORD")

    # SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    INFO_USED_DB = "production db"


configs = {
    "development": DevConfig,
    "test": TestConfig,
    "production": ProdConfig,
    "local_production": LocalProdConfig,
    "default": ProdConfig,
}
