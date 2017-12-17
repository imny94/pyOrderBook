# Import Python Packages
import multiprocessing, threading, csv, Queue
from threading import Thread

# Import Self-defined Packages
import Tree, EventList, TransactionMatcher, Database

class OrderBook():

    def __init__(self, inputQueue, inputFile = None, outputFile = None, saveOutput = False, showDisplay = False, verbose = None, maxTreeSize = None):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.saveOutput = saveOutput
        self.showDisplay = showDisplay
        self.verbose = verbose
        self.maxTreeSize = maxTreeSize
        self.inputQueue = inputQueue

    def terminateSequence(self, terminateFlag):
        print "Terminating Program ... Killing all threads"
        if terminateFlag is not None:
            terminateFlag.set()

    '''
    DESCRIPTION:
        This function will be used to update the relevant trees from csv row read in

        Row should be in format [UserID, Time, Price, NumShares, Type]
    '''
    def updateTrees(self, inputFile = None, outputFile = None, saveOutput = False, newEvent = None):
        askTree = self.askTree
        bidTree = self.bidTree
        
        ####################Nested Function####################################################
        def update(row):
            # Row should be in format [UserID, Time, Price, NumShares, Type]

            AorB = row[-1]
            temp = row[3]
            row[3] = int(temp)
            temp = row[2]
            row[2] = float(temp)
            if AorB.lower() == "ask":
                askTree.add(row)
            elif AorB.lower() == "bid":
                bidTree.add(row)
            elif AorB.lower() == "cask":
                askTree.removeOrderFromNode(row[2], row)
            elif AorB.lower() == "cbid":
                bidTree.removeOrderFromNode(row[2],row)
            else:
                print "Invalid command: %s given!"%row
                print "Type can only be 'ask','bid','cask' or 'cbid'"
                return
        ################End of Nested Function ##########################################################

        # Update the newEvent
        if newEvent != None:
            return update(newEvent)

        if saveOutput:
            if outputFile == None:
                assert False, "No output file specified!"

        if inputFile != None:
            # Read in the csv file
            with open(inputFile, "rb") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                firstRow = csvfile.readline()
                if not csv.Sniffer().has_header(firstRow):
                    print "hi"
                    update(firstRow)
                else:
                    # print "HAS HEADER!"
                    # print firstRow
                    # print csv.Sniffer().has_header(firstRow)
                    pass
                # Row should be in format [Idx(for Testing), userID, Ask/Bid, Add/Cancel, timestamp, #Shares, price]
                for row in reader:
                    update(row)

    def transactionListener(self):
        askTree = self.askTree
        bidTree = self.bidTree

        # Define constant to do error checking with the user input for new events
        numAttributes = 5

        # Listen for new transactions to be added to orderbook
        while not self.terminateFlag.isSet():
            try:
                print "transactionListener!"
                newTransaction = self.inputQueue.get(timeout = 3)
                if len(newTransaction) != numAttributes:
                    raise ValueError("Invalid Input to Orderbook!")

                self.updateTrees(newEvent=newTransaction)
            except Queue.Empty:
                pass

    '''
    DESCRIPTION:
        This function will define the thread that is responsible for matching transactions with one another

        It will create an instance of TransactionMatcher and runMatches
    '''
    def matchTransactions(self, databaseQueue, verbose = False):
        matcher = TransactionMatcher.TransactionMatcher(self.askTree, self.bidTree, databaseQueue, self.terminateFlag, verbose)
        matcher.runMatches()

    def databaseThread(self, databaseQueue, verbose):
        db = Database.EventDatabase(databaseQueue, self.terminateFlag, verbose)
        db.run()

    def run(self):
        # Initialising variables
        databaseQueue = multiprocessing.Queue(maxsize=0)
        self.askTree = Tree.Tree(1, databaseQueue, self.maxTreeSize)
        self.bidTree = Tree.Tree(0, databaseQueue, self.maxTreeSize)

        # Complete populating relevant information from csv file
    	self.updateTrees(self.inputFile, self.outputFile, self.saveOutput)

        # Flag that will be used to terminate other threads if terminate command is given
        self.terminateFlag = threading.Event()

        # Define the thread that will match up orders
        matchingThread = Thread(target=self.matchTransactions, args=(databaseQueue, self.verbose, ))
        # Define the thread that will run database slave
        databaseThread = Thread(target=self.databaseThread, args=(databaseQueue, self.verbose, ))
        # Define the thread that will take in user input
        transactionListener = Thread(target=self.transactionListener)

        # Start the different threads
        matchingThread.start()
        databaseThread.start()
        transactionListener.start()

        print "Completed running all processes!"

    def terminate(self):
        self.terminateFlag.set()