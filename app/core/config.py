import ipaddress

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    SERVER_HOST: AnyUrl | ipaddress.IPv4Address = '0.0.0.0'
    SERVER_PORT: int = 8000

    class Config(object):
        env_file = '.env'

settings = Settings()
