from flask import Flask
import pymysql
import os

import pymysql.cursors

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


    def connectOtherCursor(self): 
        connection = pymysql.connect (
            host= os.getenv("SERVERNAME"),
            user= os.getenv("DBUSER"),
            password= os.getenv("PASSWORD"),
            database= os.getenv("DBNAME"),
            cursorclass=pymysql.cursors.Cursor
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
    
    def executeQueryOtherCursor(self, query):
        connection = self.connectOtherCursor()
        with connection.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
            connection.commit()
            connection.close()
            return res

    def executeTransaction(self, queries, select = False):
        connection = self.connect()
        with connection.cursor() as cursor:
            # start the transaction
            
            cursor.execute("START TRANSACTION")
            
            result = None
            # execute all queries except the last one
            for query in queries[:-1]:
                cursor.execute(query)

            # execute the last query
            cursor.execute(queries[-1])
            if (select):
                result = cursor.fetchone()  # get the result of the last query
            else:
                result = False
            # commit the transaction
            connection.commit()
            connection.close()
            return result