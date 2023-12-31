import mysql.connector

class Interfacer:
    """
    A class representing an interfacer with the SQL Database. 

    attributes:
    _connection: MySQLConnection 
        The connection to the SQL Database.  
    _cursor: MySQLCursor
        The cursor used to query the SQL Database. 
        
    """
    def __init__(self,config):
        """ 
        Parameters 
        ----------
        config: dictionary
            a config dictionary representing the necessary 
            parameters to establish a connection to the SQL 
            server.

        Returns
        ----------
        Interfacer object

        """
        self._connection = mysql.connector.connect(**config)
        self._cursor = self._connection.cursor()

    def callproc(self,procedure,args):
        """  Calls a procedure on the SQL server.
        Parameters 
        ----------
        procedure: string
            A string representing an SQL procedure name 
        args: tuple
            A tuple of arguments for the SQL procedure

        """
        self._cursor.callproc(procedure,args)

    def execute(self,statement, args):
        """ Executes a statement on the SQL server.
        Parameters 
        ----------
        statement: string
            A string repsenting an SQL query / statement to execute
        args: tuple
            A tuple of arguments for the SQL query

        Returns
        ----------

        """
        self._cursor.execute(statement,args)

    def commit(self):
        """ Commits any changes made to the database. 
        """
        self._connection.commit()

    def fetchone(self):
        """ Fetches a single result from a query or procedure
        from the cursor
       
       Returns
        ----------
        A list containing a singular tuple that is the result of the query.

        """
        return self._cursor.fetchone()

    def fetchall(self):
        """ Fetches all results from a query or procedure 
        from the cursor

        Returns
        ----------
        An iterator over all tuples that are a result of the query.

        """
        return self._cursor.fetchall()

    def fetchmany(self,size):
        """ Fetches a fixed number of results from a query or procedure 
        from the cursor 

        Parameters 
        ----------
        size: int
            The number of results to fetch from the query

        Returns
        ----------
        An iterator over all tuples that are the result of the query 

        """
        return self._cursor.fetchmany(size)

    def close(self):
        """ Closes the active connection to the SQL server.  

        """
        self._connection.close()

