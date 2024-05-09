from flask import Flask
from dotenv import load_dotenv
import pymysql
import os

load_dotenv()
class Database:
    def connect(self):
        connection = pymysql.connect (
            host= os.getenv("SERVERNAME"),
            user= os.getenv("DBUSER"),
            password= os.getenv("PASSWORD"),
            database= os.getenv("DBNAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    def executeQuery(self, query):
        connection = self.connect()
        with connection.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
            connection.commit()
            connection.close()
            return res

