import sqlite3
import numpy as np

class DataBase():

    def __init__(self,type_of_db):
        self.connection = sqlite3.connect("Events.db")
        self.connection.text_factory = str #converting SQL output from Unicode to Bytestring
        self.cursor = self.connection.cursor()
    
    '''
    DESCRIPTION:
        creates new table if it exists
        transaction: stores transactions with following columns:
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

        if TableName == "transactions":
            sql_command = """
            CREATE TABLE IF NOT EXISTS %s ( 
            TxID INTEGER, 
            User1ID VARCHAR(20), 
            User2ID VARCHAR(20), 
            EventTime DATETIME, 
            Price NUMERIC(10,4),
            NumShares NUMERIC(10,18),
            EventType INT);"""%TableName
            #self.cursor.execute(sql_command)
        elif TableName == "bid" or TableName == "ask":
            sql_command = """
            CREATE TABLE IF NOT EXISTS %s (  
            UserID VARCHAR(20), 
            EventTime DATETIME, 
            Price NUMERIC(10,4),
            NumShares NUMERIC(10,18),
            EventType INT);"""%TableName
        else:
            print "Table name is not \"Bid\", \"Ask\", or \"Transactions\"." #if table name is not what we want
            return
        #Executing SQL command
        self.cursor.execute(sql_command)
        self.connection.commit()


    '''
    DESCRIPTION:
        Removes the table IF it exists
    '''
    def RemoveTable(self,TableName):
        # delete table from database
        TableName = TableName.lower()

        delete_command = """DROP TABLE IF EXISTS %s"""%TableName
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
            insert_command = """INSERT INTO {0} (UserID, EventTime, Price, NumShares, EventType)
            VALUES ('{1}','{2}',{3},{4},{5});""".format(TableName,Data[0],Data[1],Data[2],Data[3],Data[4])
            #UserID & Time data requires addition quote for formatting
            #self.cursor.execute(insert_command)
        #else data must have 7 arguments, its a transaction Data
        else:
            #insert transaction data into the table
            insert_command = """INSERT INTO %s (TxID, User1ID, User2ID, EventTime, Price, NumShares, EventType)
            VALUES (%s,'%s','%s','%s',%s,%s,%s);"""%(TableName,Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6]) 
            #User1ID/User2ID & Time data requires addition quote for formatting
        
        self.cursor.execute(insert_command)
        self.connection.commit()


    '''
    DESCRIPTION:
        Fetches certain number of entries
        Returns 
    '''
    def FetchKEntries(self, TableName, Quantity=1000):     #Fetch top 1,000 entry by default
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
        elif TableName == "transactions":
            self.cursor.execute("""Select * FROM {0}
            ORDER BY EventTime DESC""".format(TableName))
            print("Fetching Transaction: ")
            result = self.cursor.fetchmany(Quantity)
        else:
            print("Table not of type Ask/Bid/Transactions")
            return

        final_result = [list(i) for i in result]
        np_array = np.array(final_result)
        print np_array
            
        self.connection.commit()
        return np_array

    '''
    DESCRIPTION:
        Gets the ten latest entries from Table
    '''
    def Get10Entries(self, TableName):
        TableName = TableName.lower()

        if(TableName == "transactions"):
            np_arr = self.FetchKEntries(TableName, 10)
            extracted_arr = np_arr[:,[3,5,4]] #Time, NumShares, Price
        else:
            pass

        print extracted_arr
        return extracted_arr

    '''
    DESCRIPTION: 
        Gets all prices in descending order from particular table
        Returns: numpy array of prices
    '''
    def GetPrices(self, TableName):
        TableName = TableName.lower()

        self.cursor.execute("""Select Price From {0}
        ORDER By Price DESC""".format(TableName))

        result = self.cursor.fetchall()
        self.connection.commit()

        final_result = [list(i)[0] for i in result]
        np_array = np.array(final_result)

        #print("np aray for prices: ")
        #print np_array
        return np_array

    #Close the Database
    def CloseConnection(self):
        #Close the Database
        sqlite3.connect("Events.db").close()


'''

#Test cases
def main():
    database = DataBase("")
    database.NewTable("transactions")
    # database.RemoveTable("transaction")

    # database.InsertData("ask",("1", "1111-11-11 11:11.11.254","89", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.574","100", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.124","77", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.125","90", "1", "2"))
    # database.InsertData("ask",("1", "1111-11-11 11:11.11.344","67", "1", "2"))
    # database.FetchData("ask")

    database.InsertData("transactions",("1", "Alice" , "Bob", "1111-11-11 11:11.11.111","97", "1", "2"))
    database.InsertData("transactions",("1", "Bob" , "Clarice", "1111-11-11 11:11.11.112","107", "1", "2"))
    database.InsertData("transactions",("1", "Dominic" , "Ellen", "1111-11-11 11:11.11.113","127", "1", "2"))
    database.InsertData("transactions",("1", "Fabian" , "Germaine", "1111-11-11 11:11.11.114","167", "1", "2"))
    database.InsertData("transactions",("1", "Ellen" , "Fabian", "1111-11-11 11:11.11.115","77", "1", "2"))
    database.FetchKEntries("transactions")
    database.GetPrices("transactions")
    database.Get10Entries("transactions")
    database.CloseConnection()
    database.RemoveTable("transactions")


if __name__ == '__main__':
	main()
'''