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

    def call_stored_procedure(self):
        try:
            cursor = self.__mydb.cursor()
            cursor.callproc('updateTitle', [])
            # print results
            for result in cursor.stored_results():
                return result.fetchall()
        except mysql.connector.Error as error:
            print("Failed to execute stored procedure: {}".format(error))
        finally:
            cursor.close()

    def insert_person(self, first_name, last_name, age, address):
        try:
            cursor = self.__mydb.cursor()
            self.__mydb.start_transaction()
            sql = "INSERT INTO persons (first_name, last_name, age, address) VALUES (%s, %s, %s, %s)"
            val = (first_name, last_name, age, address)
            cursor.execute(sql, val)
            self.__mydb.commit()
            print(cursor.rowcount, "record inserted.")
            return cursor.rowcount

        except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            self.__mydb.rollback()  # reverting changes because of exception

        finally:
            cursor.close()

    def shutdown_db(self):
        self.__mydb.close()

    def __init__(self):
        self.__mydb = mysql.connector.connect(
            host="localhost",
            user=config('MYSQL_USER'),
            passwd=config('PASSWORD'),
            database="Book_Store"
        )

        self.__mydb.autocommit = False

