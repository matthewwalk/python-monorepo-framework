import psycopg2
from utils.utils import defaulter
import logging

class db():

    
    def __init__(self) -> None:
        config = {
            "database" : defaulter("POSTGRES_DB", "db"),
            "user" : defaulter("POSTGRES_USER", "admin"),
            "password" : defaulter("POSTGRES_PASSWORD", "admin"),
            "host" : defaulter("POSTGRES_HOST", "postgres"),
            "port" : defaulter("POSTGRES_PORT", 5432)
        }
        self.logger = logging.getLogger('db')
        self.logger.info('initializing db ...')
        self.conn = psycopg2.connect(**config)

    
    def execute(self, statement) -> list[tuple]:
        self.logger.debug(f'execute request recieved : statement={statement}')
        cur = self.conn.cursor()
        cur.execute(query=statement)
        return cur.fetchall()