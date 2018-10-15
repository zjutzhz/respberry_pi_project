class Config(object):
    pass
class ProdConfig(object):
    pass
class DevConfig(object):
    DEBUG=True
    MAX_CONTENT_LENGTH=1600 * 1024 * 1024
    # SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
