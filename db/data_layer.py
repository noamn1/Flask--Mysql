import mysql.connector
from decouple import config


class DataLayer:

    def get_person_by_id(self, id):
        try:
            cursor = self.__mydb.cursor()
            sql = "SELECT first_name,last_name,age,address FROM persons WHERE id=%s"
            cursor.execute(sql, (id,))
            res = cursor.fetchone()
            return res
        finally:
            cursor.close()

    def get_person_by_last_name(self, last_name):
        try:
            cursor = self.__mydb.cursor()
            results = []
            sql = "SELECT first_name,last_name,age,address FROM persons WHERE last_name=%s"
            cursor.execute(sql, (last_name,))
            for (first_name, last_name, age, address) in cursor:
                results.append({"first_name": first_name, "last_name": last_name, "age": age, "address": address})

            return results
        finally:
            cursor.close()

    def insert_person(self, first_name, last_name, age, address):
        try:
            cursor = self.__mydb.cursor()
            sql = "INSERT INTO persons (first_name, last_name, age, address) VALUES (%s, %s, %s, %s)"
            val = (first_name, last_name, age, address)
            cursor.execute(sql, val)
            self.__mydb.commit()
            print(cursor.rowcount, "record inserted.")
            return cursor.rowcount
        finally:
            cursor.close()

    def shutdown_db(self):
        self.__mydb.close()

    def __init__(self):
        self.__mydb = mysql.connector.connect(
            host="localhost",
            user=config('MYSQL_USER'),
            passwd=config('PASSWORD'),
            database="ITC"
        )

