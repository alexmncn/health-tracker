"""Application configuration."""
from environs import Env

env = Env()
env.read_env()

HOSTNAME = env.str("HOSTNAME")

SECRET_KEY = env.str("SECRET_KEY")


SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False


PUSHOVER_APP_TOKEN = env.str("PUSHOVER_APP_TOKEN")
PUSHOVER_USER_KEY = env.str("PUSHOVER_USER_KEY")


class NOIP_DNS:
    URL = env.str("NOIP_DNS_URL")
    HOSTNAME = HOSTNAME
    USERNAME = env.str("NOIP_DNS_USERNAME")
    PASSWORD = env.str("NOIP_DNS_PASSWORD")