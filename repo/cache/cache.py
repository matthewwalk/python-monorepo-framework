import redis
import logging
from utils.utils import defaulter


config = {
    'host': defaulter("REDIS_HOST", "localhost"),
    'port': defaulter("REDIS_PORT", 6379),
    'db' :  defaulter("REDIS_DB", 0)
}


class cache():


    def __init__(self) -> None:
        self.logger = logging.getLogger('cache')
        self.logger.info('initializing cache ...')
        self.client = redis.Redis(**config)


    def set(self, key, value) -> bool:
        self.logger.debug(f'set request recieved : key={key}, value={value}')
        return self.client.set(key, value)


    def get(self, key) -> str:
        self.logger.debug(f'get request recieved : key={key}')
        return self.client.get(key)
        