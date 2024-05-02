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

    def executeTransaction(self, queries):
        with self.connection.cursor()as cursor:
            # start the transaction
            
            cursor.execute("START TRANSACTION")
            
            result = None
            # execute all queries except the last one
            for query in queries[:-1]:
                cursor.execute(query)

            # execute the last query
            cursor.execute(queries[-1])
            result = cursor.fetchone()  # get the result of the last query

            # commit the transaction
            #self.connection.commit()

            return result
        

    def closeConnection(self):
        self.connection.close()