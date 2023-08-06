import mysql.connector as sql
import pandas as pd
from datetime import datetime
from pytz import timezone
import paramiko
from paramiko import SSHClient
from scp import SCPClient
# import logging
class MysqlConnector:
    """Instantiate a DB connector.
    Args:
        host (str): Database host 
        port (str): Database port
        user (str): Username
        password (str): Password
        allow_local_infile (boolean): Local infile is allowed when the value is True
    Returns:
        result (str): Value is 'OK' when successful
    """   
    
    def __init__(self, host, port, user, password, allow_local_infile=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.allow_local_infile = allow_local_infile
        
        self.db_connection = sql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            ssl_disabled=True,
            autocommit=True,
            allow_local_infile=True
        )    
        self.db_cursor = self.db_connection.cursor()
        if allow_local_infile:
            query_str = """SET GLOBAL local_infile=1"""
            self.db_cursor.execute(query_str)
        
    def query_without_fetch(self, query_str):
        """
        Send non DQL query
        Args:
            query_str (str): sql query
        Returns:
            result (str): Value is 'OK' when successful
        """
        self.db_cursor.execute(query_str)
        return 'OK'
    
    def query_to_dataframe(self, query_str):
        """
        Query and store the result in a dataframe
        Args:
            query_str (str): sql query
        Returns:
            result (dataframe): Result in a dataframe
        """
        self.db_cursor.execute(query_str)
        table_rows = self.db_cursor.fetchall()
        df = pd.DataFrame(table_rows, columns=self.db_cursor.column_names)
        return df
    
    def load_csv(
        self,
        db_name, 
        table_name, 
        file_name,
        write_disposition,
        delimiter=',', 
        ignore_rows=1,
        is_local_csv=True
    ):
        """
        Load a local CSV file into a table
        Args:
            db_name (str): Database name where the CSV will be loaded
            table_name (str): Table name where the CSV will be loaded
            file_name (str): CSV file name
            delimiter (str): CSV delimiter character
            ignore_rows (str): Number of rows that will be ignored from the top
            write_disposition (str): Write method to add data into table (WRITE_TRUNCATE, WRITE_APPEND)
            is_local_csv (boolean): If the value is True, then CSV file is in local machine. If the value is False, then CSV file is in remote machine.
        Returns:
            result (str): The result of function
        """
        result = ''

        if write_disposition == 'WRITE_TRUNCATE':
            query = 'TRUNCATE TABLE {db_name}.{table_name}'.format(db_name=db_name, table_name=table_name)
            self.db_cursor.execute(query)
            self.db_connection.commit()

        # load table
        if is_local_csv:
            sql_import_table = (""" LOAD DATA LOCAL INFILE '{file_name}' 
                                    INTO TABLE {db_name}.{table_name}
                                    FIELDS TERMINATED BY '{delimiter}' 
                                    LINES TERMINATED BY '\\n'
                                    IGNORE {ignore_rows} ROWS;
            """).format(file_name=file_name, db_name=db_name, table_name=table_name, delimiter=delimiter, ignore_rows=ignore_rows)
        else:
            sql_import_table = (""" LOAD DATA INFILE '{file_name}' 
                                    INTO TABLE {db_name}.{table_name}
                                    FIELDS TERMINATED BY '{delimiter}' 
                                    LINES TERMINATED BY '\\n'
                                    IGNORE {ignore_rows} ROWS;
            """).format(file_name=file_name, db_name=db_name, table_name=table_name, delimiter=delimiter, ignore_rows=ignore_rows)
            
        self.db_cursor.execute(sql_import_table)
        self.db_connection.commit()
        result = 'OK'
        return result