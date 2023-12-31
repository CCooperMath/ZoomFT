import mysql.connector

class Interfacer:
    def __init__(self,config):
        self._connection = mysql.connector.connect(**config)
        self._cursor = self._connection.cursor()

    def callproc(self,procedure,args):
        self._cursor.callproc(procedure,args)

    def execute(self,statement, args):
        self._cursor.execute(statement,args)

    def commit(self):
        self._connection.commit()

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def fetchmany(self,size):
        return self._cursor.fetchmany(size)

    def close(self):
        self._connection.close()

