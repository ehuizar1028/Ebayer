import sqlite3
connection = sqlite3.connect("EbayData.db")

class sqliter:
    def __init__(self):
        pass

    def setupConnection(self):
        self.cursor = connection.cursor()

    def recreateTable(self):
        sql_command = """
        CREATE TABLE keywords ( 
        keywordID INTEGER PRIMARY KEY, 
        keyword VARCHAR(20), 
        category VARCHAR(30),
        timestamp datetime); 
        """

    def purge(self):
        # delete
        self.cursor.execute("""DROP TABLE keywords;""")

    def insert(self, sql_command):
        self.cursor.execute(sql_command)
        connection.commit()

    def select(self, sql_command):
        self.cursor.execute(sql_command)
        return self.cursor.fetchall()

    def close(self):
        connection.close()
