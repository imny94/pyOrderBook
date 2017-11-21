import sqlite3


class DataBase():

    def __init__(self,type_of_db):
        self.connection = sqlite3.connect("Transaction.db")
        self.connection.text_factory = str #converting SQL output from Unicode to Bytestring
        self.cursor = self.connection.cursor()
    
    '''
    DESCRIPTION:
        creates new table if it exists
        successful: stores transactions with following columns:
            txID: transaction ID
            User1ID: user1
            User2ID: user2
            EventTime: time of transaction
            Price: price at which stock is successfully traded
            NumShares: number of shares traded
            Type: 2 for transaction
    '''
    def NewTable(self, TableName):
        #Specifying SQL command to create table and defining fields
        TableName = TableName.lower()

        if  TableName == "successful":
            sql_command = """
            CREATE TABLE IF NOT EXISTS %s ( 
            TxID INTEGER, 
            User1ID VARCHAR(20), 
            User2ID VARCHAR(20), 
            EventTime DATETIME, 
            Price NUMERIC(10,4),
            NumShares NUMERIC(10,18),
            Type INT);"""%TableName
            #Executing SQL command
            self.cursor.execute(sql_command)

        elif TableName == "bid" or TableName == "ask":
            sql_command = """
            CREATE TABLE IF NOT EXISTS %s (  
            UserID VARCHAR(20), 
            EventTime DATETIME, 
            Price NUMERIC(10,4),
            NumShares NUMERIC(10,18),
            Type INT);"""%TableName
            #Executing SQL command
            self.cursor.execute(sql_command)
            
        else:
            print "Table name is not \"Bid\", \"Ask\", or \"Successful\"." #if table name is not what we want
            pass
        self.connection.commit()


    '''
    DESCRIPTION:
        Removes the table IF it exists
    '''
    def RemoveTable(self,DropTableName):
        # delete table from database
        delete_command = """DROP TABLE IF EXISTS %s""" %DropTableName
        #Executing SQL command
        self.cursor.execute(delete_command)
        self.connection.commit()

    '''
    DESCRIPTION:
        Adds event into the Table
    '''
    def InsertData(self,TableName,Data):

        TableName = TableName.lower()
        #if data has 5 arguments, its a Ask/Bid Data
        if len(Data) == 5:
            #Insert Ask/Bid Data into the table
            insert_command = """INSERT INTO {0} (UserID, EventTime, Price, NumShares, Type)
            VALUES ('{1}','{2}',{3},{4},{5});""".format(TableName,Data[0],Data[1],Data[2],Data[3],Data[4])
            #UserID & Time data requires addition quote for formatting
            self.cursor.execute(insert_command)
        #else data must have 7 arguments, its a successful Data
        else:
            #insert successful data into the table
            insert_command = """INSERT INTO %s (TxID, User1ID, User2ID, EventTime, Price, NumShares, Type)
            VALUES (%s,'%s','%s','%s',%s,%s,%s);"""%(TableName,Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6]) 
            #User1ID/User2ID & Time data requires addition quote for formatting
            self.cursor.execute(insert_command)
        self.connection.commit()


    '''
    DESCRIPTION:
        Fetches certain number of entries
        Returns 
    '''
    def FetchData(self, TableName, Quantity=1000):     #Fetch top 1,000 entry by default
        #Highest Bid first
        TableName = TableName.lower()

        if TableName == "bid":
            self.cursor.execute("""Select * FROM {0}
            ORDER BY Price, EventTime DESC""".format(TableName))
            print("Fetching Bids: ")
            result = self.cursor.fetchmany(Quantity)
        #Lowest Ask first
        elif TableName == "ask":
            self.cursor.execute("""Select * FROM {0}
            ORDER BY Price, EventTime ASC""".format(TableName))
            print("Fetching Asks: ")
            result = self.cursor.fetchmany(Quantity)
        #Latest Transaction first
        elif TableName == "successful":
            self.cursor.execute("""Select * FROM {0}
            ORDER BY EventTime DESC""".format(TableName))
            print("Fetching Transaction: ")
            result = self.cursor.fetchmany(Quantity)
        else:
            print("Table not of type Ask/Bid/Transaction")
            return

        final_result = [list(i) for i in result]
        print final_result
            
        self.connection.commit()
        return final_result
    
    #Close the Database
    def CloseConnection(self):
        #Close the Database
        sqlite3.connect("Transaction.db").close()


'''

#Test cases
def main():
    database = DataBase("")
    database.NewTable("Successful")
    # database.RemoveTable("Successful")

    # database.InsertData("Successful",("1", "1111-11-11 11:11.11.254","89", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.574","100", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.124","77", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.125","90", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.344","67", "1", "2"))
    # database.FetchData("ask")

    database.InsertData("Successful",("1", "Alice" , "Bob", "1111-11-11 11:11.11.111","97", "1", "2"))
    database.InsertData("Successful",("1", "Bob" , "Clarice", "1111-11-11 11:11.11.112","107", "1", "2"))
    database.InsertData("Successful",("1", "Dominic" , "Ellen", "1111-11-11 11:11.11.113","127", "1", "2"))
    database.InsertData("Successful",("1", "Fabian" , "Germaine", "1111-11-11 11:11.11.114","167", "1", "2"))
    database.InsertData("Successful",("1", "Ellen" , "Fabian", "1111-11-11 11:11.11.115","77", "1", "2"))
    database.FetchData("Successful")
    database.CloseConnection()
    database.RemoveTable("Successful")


if __name__ == '__main__':
	main()

'''