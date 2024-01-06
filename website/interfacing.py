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


    def commit(self):
        """ Commits any changes made to the database. 
        """
        self._connection.commit()

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

    def getID(self,table,field,reference):
        """ Grabs an id from the SQL database from a set table using a certain
        field and reference to match. 

        Parameters
        ----------
        table : string
            The name of the table to check.
        
        field : string
            The name of the field to check against.

        reference: any
            The value to reference with the field. 
        
        Returns 
        ----------
        entryID: int
            the id from the table which matches the reference in the given field.

        """
        query = f'SELECT * FROM {table} WHERE {field} = %s'
        self.execute(query, (reference, ))
        if((result := self.fetchall()) != None):
            return result[0][0]
        else:
            return None

    def getFromReference(self,table,field,reference):
        """ Grabs rows from the SQL database that match the value reference in 
        the specified field

        Parameters
        ----------
        table: string 
            The name of the table to check.
        field: string  
            The name of the field to check
        reference: any
            The value to reference with the field. 

        Returns 
        -------
        An iterator over all tuples representing the result of the query. Returns
        None in the case the result is empty. 

        """

        query = f'SELECT * FROM {table} WHERE {field}=%s'
        self.execute(query, (reference, ))
        return self.fetchall() 




    def getFromID(self,table,entryID):
        """ Grabs an id from the SQL database from a set table using a certain
        field and reference to match. 

        Parameters
        ----------
        table : string
            The name of the table to check.
        
        field : string
            The name of the field to check against.

        reference: any
            The value to reference with the field. 
        
        Returns 
        ----------
        A tuple representing the fetched value from the ID. 
        """

        query = f'SELECT * FROM {table} WHERE id = %s'

        self.execute(query, (entryID, ))
        result = self.fetchall()
        if(result):
            return result[0]
        else:
            return None

    def deleteFromReference(self,table, field, reference):
        """ Deletes all values from a table which have value 'reference' 
        in a given field. 

        Parameters 
        ----------
        table: string
            The table to delete from.
        field: string
            The field to check against.
        reference: any
            The reference value to use.
        
        Returns 
        ----------
        True if the value is successfully deleted. False otherwise. 
        """
        query = f'DELETE FROM {table} WHERE {field} = %s'
        try:
            self.execute(query, (reference, ))
            return True
        except Exception as e:
            print(e)
            return False

    def getRelated(self,joinTable, extTable, idRefName,idExtName, refID):
        """ Fetches all elements of a secondary table using a many-to-many join table where the 
        reference ID matches the reference field.

        Parameters
        ----------
        joinTable: string
            The name of the jointable which connects the two categories. 
        extTable: string
            The name of the table we are finding connections to. 
        idRefName: string
            The name of the id being used to reference the join table. 
        idExtName: string
            The name of the id used to connect to the external table in the join table.
        refID: int
            The id of the item we are referencing.

        Returns 
        ----------
        An iterator over all elements related to the referenceID in the external table. None if 
        empty and None if the request failed. 
        """
        
        query = f'SELECT * FROM ({joinTable} INNER JOIN {extTable} ON {joinTable}.{idRefName} = %s AND {joinTable}.{idExtName} = {extTable}.id)'
        try:
            self.execute(query,(refID, ))
            return self.fetchall()
        except Exception as e:
            print(e)
            return None

    def addRelation(self,joinTable, idName1, idName2, id1, id2):
        """
        Adds a relationship between two elements having ids id1 and id2 to the SQL Database 
        in joinTable. 

        Parameters
        ----------
        joinTable: string
            A string representing the name of the jointable holding a relationship
            between the two ids 
        id1: int 
            The id of the first value.
        id2: int
            The id of the second value.

        Returns 
        ----------
        True if the relationship was successfully added. False if otherwise. 
        """
        query = f'INSERT INTO {joinTable}({idName1},{idName2}) VALUES (%s,%s)'
        try: 
            self.execute(query, (id1, id2))
            return True
        except Exception as e:
            print(e)
            return False


    def removeRelated(self,joinTable, idName1, id1):
        """ Removes ALL related elements from a join table where idName1 = id1.

        Parameters
        ----------

        Returns 
        ----------
        True upon a successful deletion. False if otherwise.
        """
        query = f'DELETE FROM {joinTable} WHERE {idName1} = %s'
        try: 
            self.execute(query, (id1, ))
            return True
        except Exception as e:
            print(e)
            return False

    def removeRelation(self,joinTable, idName1, idName2, id1,id2):
        """
        Removes a relationship between two elements having ids id1 and id2 to the SQL Database 
        in joinTable. 

        Parameters
        ----------
        joinTable: string
            A string representing the name of the jointable holding a relationship
            between the two ids 
        id1: int 
            The id of the first value.
        id2: int
            The id of the second value.

        Returns 
        ----------
        True if the relationship was successfully removed. False if otherwise. 
        """
        query = f'DELETE FROM {joinTable} WHERE {idName1} = %s AND {idName2} = %s' 
        try:
            self.execute(query, (id1, id2))
            return True
        except Exception as e:
            print(e)
            return False

    def editEntry(self,table, refField, editField, refVal, editVal):
        """ Edits an entry of the SQL database in a table where the 
        reference value matches in the reference field from its current
        value to a new value. 

        Parameters
        ----------
        table: string
            The name of the table to edit.
        refField: string
            The reference field to check against.
        editField: string
            The field to edit. 
        refVal: any
            The value to check the reference field against.
        editVal: any 
            The new value for the edited field. 

        Returns 
        -------
        True if successful. False if otherwise. 
        """

        query = f'UPDATE {table} SET {editField} = %s WHERE {refField} = %s'
        try:
            self.execute(query, (editVal,refVal))
            self.commit()
            return True
        except Exception as e:
            print(e)
            return False

        



