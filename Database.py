import numpy as np
import sqlite3
import logging, Queue


class EventDatabase():

    def __init__(self, databaseQueue = None, terminateFlag = None, verbose = None):
        self.connection = sqlite3.connect("Events.db")
        self.connection.text_factory = str #converting SQL output from Unicode to Bytestring
        self.cursor = self.connection.cursor()
        self.databaseQueue = databaseQueue
        self.terminateFlag = terminateFlag
        self.verbose = verbose

        self.NewTable("transactions")
        self.NewTable("ask")
        self.NewTable("bid")

    def __queryQueue(self):
        try:
            newEntry = self.databaseQueue.get(timeout=3)
            TableName, Data = newEntry
            if TableName[0] == "c":
                TableName = TableName[1:]
                self.RemoveEntry(TableName, Data[0])
            else:
                self.InsertData(TableName, Data)
        except Queue.Empty:
            self.debugLog("Queue Timeout!")

    def debugLog(self,msg):
        if self.verbose:
            logging.debug(msg)

    def run(self):
        while 1:
            if self.terminateFlag.isSet():
                self.debugLog("Terminating Thread!")
                break
            self.__queryQueue()

    '''
    DESCRIPTION:
        creates new table if it exists
        transaction: stores transactions with following columns:
            EventID: transaction ID
            AskID: user1
            BidID: user2
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
            EventID INTEGER PRIMARY KEY AUTOINCREMENT, 
            AskID VARCHAR(20), 
            BidID VARCHAR(20), 
            EventTime DATETIME, 
            Price NUMERIC(10,4),
            NumShares NUMERIC(10,18),
            TotalProfit NUMERIC(10,4),
            EventType INT);"""%TableName
            #self.cursor.execute(sql_command)
        elif TableName == "bid" or TableName == "ask":
            sql_command = """
            CREATE TABLE IF NOT EXISTS %s (  
            EventID VARCHAR(255) PRIMARY KEY,
            UserID VARCHAR(20), 
            EventTime DATETIME, 
            Price NUMERIC(10,4),
            NumShares NUMERIC(10,18),
            EventType INT);"""%TableName
        else:
            self.debugLog("Table name is not \"Bid\", \"Ask\", or \"Transactions\".") #if table name is not what we want
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
        #if data has 6 arguments, its a Ask/Bid Data
        if len(Data) == 6:
            #Insert Ask/Bid Data into the table
            #insert_command = """INSERT INTO {0} (EventID, UserID, EventTime, Price, NumShares, EventType)
            #VALUES ('{1}','{2}',{3},{4},{5},{6});""".format(TableName,Data[0],Data[1],Data[2],Data[3],Data[4],Data[5])
            insert_command = """INSERT INTO %s (EventID, UserID, EventTime, Price, NumShares, EventType)
            VALUES (?,?,?,?,?,?);"""%TableName

            #UserID & Time data requires addition quote for formatting
            self.cursor.execute(insert_command, (Data[0],Data[1],Data[2],Data[3],Data[4],Data[5]))
        #else data must have 7 arguments, its a transaction Data
        else:
            #insert transaction data into the table
            insert_command = """INSERT INTO %s (AskID, BidID, EventTime, Price, NumShares, TotalProfit, EventType)
            VALUES (?,?,?,?,?,?,?);"""%TableName
            #AskID/BidID & Time data requires addition quote for formatting
            self.cursor.execute(insert_command, (Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6]))
        self.connection.commit()

    '''
    DESCRIPTION:
        Remove event from table
    ''' 
    def RemoveEntry(self, TableName, entryID):
        TableName = TableName.lower()
        self.cursor.execute("SELECT * FROM %s WHERE EventID=?"%TableName,(entryID,))
        data = self.cursor.fetchone()
        if data is None:
            self.debugLog('There is no event with eventID %s'%entryID)
            return
        else:
            self.cursor.execute("DELETE FROM %s WHERE EventID=?"%TableName,(entryID,))
            return list(data)

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
            self.debugLog("Fetching Bids: ")
            result = self.cursor.fetchmany(Quantity)
        #Lowest Ask first
        elif TableName == "ask":
            self.cursor.execute("""Select * FROM {0}
            ORDER BY Price, EventTime ASC""".format(TableName))
            self.debugLog("Fetching Asks: ")
            result = self.cursor.fetchmany(Quantity)
        #Latest Transaction first
        elif TableName == "transactions":
            self.cursor.execute("""Select * FROM {0}
            ORDER BY EventTime DESC""".format(TableName))
            self.debugLog("Fetching Transaction: ")
            result = self.cursor.fetchmany(Quantity)
        else:
            self.debugLog("Table not of type Ask/Bid/Transactions")
            return

        final_result = [list(i) for i in result]
        np_array = np.array(final_result)
        self.debugLog(np_array)
            
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

        self.debugLog(extracted_arr)
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



#Test cases
def main():
    import threading
    database = EventDatabase(Queue.Queue(), threading.Event(), True)

    ###
    #Test ask/bid
    ###

    # database.NewTable("ask")
    # database.InsertData("ask",("abc123", "Alice", "1111-11-11 11:11.11.254","89", "1", "2"))
    # database.InsertData("ask",("aab123", "Bob", "1111-11-11 11:11.11.574","100", "1", "2"))
    # database.InsertData("ask",("aaa123", "Cat", "1111-11-11 11:11.11.124","77", "1", "2"))
    # database.InsertData("ask",("abcd123", "Joe", "1111-11-11 11:11.11.125","90", "1", "2"))
    # database.InsertData("ask",("a123", "Zoe", "1111-11-11 11:11.11.344","67", "1", "2"))
    # mydata = database.RemoveEntry("ask","abc123")
    # print mydata
    # database.FetchKEntries("ask")
    # database.RemoveTable("ask")



    ###
    #Test transactions
    ###

    database.NewTable("transactions")
    database.InsertData("transactions",("Alice" , "Bob", "1111-11-11 11:11.11.111","97", "1", "30", "2"))
    database.InsertData("transactions",("Bob" , "Clarice", "1111-11-11 11:11.11.112","107", "1", "40", "2"))
    database.InsertData("transactions",("Dominic" , "Ellen", "1111-11-11 11:11.11.113","127", "1", "50", "2"))
    database.InsertData("transactions",("Fabian" , "Germaine", "1111-11-11 11:11.11.114","167", "1", "60", "2"))
    database.InsertData("transactions",("Ellen" , "Fabian", "1111-11-11 11:11.11.115","77", "1", "70", "2"))
    # database.FetchKEntries("transactions")
    # database.GetPrices("transactions")
    # database.Get10Entries("transactions")
    mydata = database.RemoveEntry("transactions", "1")
    print mydata
    database.FetchKEntries("transactions")
    database.CloseConnection()
    database.RemoveTable("transactions")

if __name__ == '__main__':
	main()
