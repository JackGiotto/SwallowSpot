from flask import Flask
from dotenv import load_dotenv
import pymysql
import os

load_dotenv()
class Database:
    def __init__(self):
        self.connection = pymysql.connect (
            host= os.getenv("SERVERNAME"),
            user= os.getenv("DBUSER"),
            password= os.getenv("PASSWORD"),
            database= os.getenv("DBNAME"),
            cursorclass=pymysql.cursors.DictCursor
        )

    def executeQuery(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
            self.connection.commit()
            return res

    def closeConnection(self):
        self.connection.close()