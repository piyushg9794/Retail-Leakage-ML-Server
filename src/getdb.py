import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Db:

    def __init__(self):
        pass

    def connect(self, buff=False):
        self.cnx = mysql.connector.connect(user= os.getenv('MYSQL_USER'),
                            password= os.getenv('MYSQL_PASSWORD'),
                            host= os.getenv('MYSQL_HOST'),
                            database= os.getenv('MYSQL_DATABASE'))
        self.cursor = self.cnx.cursor(buffered=buff)

        return self.cursor

    def disconnect(self):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()