import sqlite3


class DataBase():

    def __init__(self,type_of_db):
        self.connection = sqlite3.connect("Transaction.db")
        self.cursor = self.connection.cursor()
    
    def NewTable(self, TableName):
        #Specifying SQL command to create table and defining fields
        if  TableName.lower() == "successful":
            sql_command = """
            CREATE TABLE %s ( 
            TxID INTEGER PRIMARY KEY, 
            User1ID VARCHAR(20), 
            User2ID VARCHAR(20), 
            Time DATETIME, 
            Price NUMERIC(10,4),
            NumShares NUMERIC(10,18),
            Type INT);"""%TableName
            #Executing SQL command
            self.cursor.execute(sql_command)

        elif TableName.lower() == "bid" or TableName.lower() == "ask":
            sql_command = """
            CREATE TABLE %s (  
            UserID VARCHAR(20), 
            Time DATETIME, 
            Price NUMERIC(10,4),
            NumShares NUMERIC(10,18),
            Type INT);"""%TableName
            #Executing SQL command
            self.cursor.execute(sql_command)
            
        else:
            print "Table name is not \"Bid\", \"Ask\", or \"Successful\"." #if table name is not what we want
            pass
        self.connection.commit()

    def RemoveTable(self,DropTableName):
        # delete table from database
        delete_command = """DROP TABLE %s""" %DropTableName
        #Executing SQL command
        self.cursor.execute(delete_command)
        self.connection.commit()

    def InsertData(self,TableName,Data):
        #if data has 5 arguments, its a Ask/Bid Data
        if len(Data) == 5:
            #Insert Ask/Bid Data into the table
            insert_command = """INSERT INTO {0} (UserID, Time, Price, NumShares, Type)
            VALUES ('{1}','{2}',{3},{4},{5});""".format(TableName,Data[0],Data[1],Data[2],Data[3],Data[4])
            #UserID & Time data requires addition quote for formatting
            self.cursor.execute(insert_command)
        #else data must have 7 arguments, its a successful Data
        else:
            #insert successful data into the table
            insert_command = """INSERT INTO {0} (TxID, User1ID, User2ID, Time, Price, NumShares, Type)
            VALUES ({1},'{2}','{3}','{4}',{5},{6},{7});""".format(TableName,Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6])
            #User1ID/User2ID & Time data requires addition quote for formatting
            self.cursor.execute(insert_command)
        self.connection.commit()

    def FetchData(self, TableName, Quantity=1000):     #Fetch top 1,000 entry by default
        #Highest Bid first
        if TableName == "bid":
            self.cursor.execute("""Select * FROM {0}
            ORDER BY Price DESC""".format(TableName))
            print("Fetching Bids: ")
            result = self.cursor.fetchmany(Quantity)
        #Lowest Ask first
        elif TableName == "ask":
            self.cursor.execute("""Select * FROM {0}
            ORDER BY Price ASC""".format(TableName))
            print("Fetching Asks: ")
            result = self.cursor.fetchmany(Quantity)
        #Latest Transaction first
        else:
            self.cursor.execute("""Select * FROM {0}
            ORDER BY Time DESC""".format(TableName))
            print("Fetching Transaction: ")
            result = self.cursor.fetchmany(Quantity)
        #Test the fetched data
        for r in result:
            print(r) 
        
        self.connection.commit()
    
    #Close the Database
    sqlite3.connect("Transaction.db").close()

#Test cases
def main():
    database = DataBase("")
    # database.NewTable("Ask")
    # database.RemoveTable("Ask")

    # database.InsertData("ask",("1", "1111-11-11 11:11.11.111","89", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.111","100", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.111","77", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.111","90", "1", "2"))
    # database.InsertData("ask",("1","1111-11-11 11:11.11.111","67", "1", "2"))

    # database.InsertData("Successful",("1", "Alice" , "Bob", "1111-11-11 11:11.11.111","67", "1", "2"))
    database.FetchData("ask")
    
if __name__ == '__main__':
	main()