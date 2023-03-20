import pymysql
import os
from dotenv import load_dotenv





class Sql:
    """
    The process is to be simple 7 steps:
    - Create connection
    - Create cursor
    - Create Query string
    - Execute the query
    - Commit to the query
    - Close the cursor
    - Close the connection
    """

    instance = None
    db = pymysql
    load_dotenv()

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
            print('Instance created')
        else:
            print('Instance already created')
        return cls.instance

    def __init__(self):
        self.host = os.getenv('db_host')
        self.port = int(os.getenv('db_port'))
        self.user = os.getenv('db_user')
        self.password = os.getenv('db_password')
        self.database = os.getenv('db_name')
        self.connection = self.initiate_connection()
        self.cursor = self.create_cursor()

    def initiate_connection(self):
        connection = self.db.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=self.db.cursors.DictCursor
        )
        print('Connection istablished')
        return connection

    def create_cursor(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT @@VERSION')
        print(f'Version: {cursor.fetchone()["@@VERSION"]}')
        return cursor

    def __del__(self):
        self.cursor.close()
        self.connection.close()
        print('Connection closed')

    @staticmethod
    def neat_print(func):
        def wrapper(self, query):
            for key, item in func(self, query).items():
                print(key.ljust(30, '_'), item)
        return wrapper

    @neat_print
    def select_one(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def select_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return 'Success'
