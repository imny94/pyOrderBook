import sys, getopt, csv, time, threading, multiprocessing
from threading import Thread

from Display import display
import Tree
import EventList
import TransactionMatcher

'''
DESCRIPTION:
	This function will be used to update the relevant trees from csv row read in

	Row should be in format [UserID, Time, Price, NumShares, Type]
'''
def updateTrees(askTree, bidTree, inputFile = None, outputFile = None, saveOutput = False, newEvent = None):
	
	####################Nested Function####################################################
	def update(row):
		# e.g of row = (,0,0,1,2017/2/9,100,30)

		AorB = row[-1]
		if AorB.lower() == "ask":
			askTree.add(row)
		elif AorB.lower() == "bid":
			bidTree.add(row)
		else:
			assert False, "Invalid command: %s given!"%row
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
				print "HAS HEADER!"
				print firstRow
				print csv.Sniffer().has_header(firstRow)
			# Row should be in format [Idx(for Testing), userID, Ask/Bid, Add/Cancel, timestamp, #Shares, price]
			for row in reader:
				update(row)
	

'''
DESCRIPTION:

	This function will initialise the required variables
		- The different binary trees that will be used to store the prices for different bidding price/asking price, along with the relevant transactions poised to happen for that given price
			- Ask Tree
			- Bid Tree
		- The EventList that will be used to record and store events

	 
	This function will:
		Insert events into EventList
		Update ask and bid Trees

ARGUMENTS:
	askTree - Reference to askTree
	bidTree - Reference to bidTree
	eventList - Reference to eventList
	
'''
def orderBook(askTree, bidTree, eventList, inputFile, numThreads, outputFile = None, saveOutput = False):

	if inputFile == None:
		assert False, "No input file for commands given!"

	if saveOutput:
		if outputFile == None:
			assert False, "No output file specified!"

	# Read in the csv file
	with open(inputFile, "rb") as csvfile:
		reader = csv.reader(csvfile)
		firstRow = csvfile.readline()
		if not csv.Sniffer().has_header(firstRow):
			updateTreesAndEventList(askTree, bidTree, eventList, firstRow)
		# Row should be in format [Idx(for Testing), userID, Ask/Bid, Add/Cancel, timestamp, #Shares, price]
		for row in reader:
			updateTreesAndEventList(askTree, bidTree, eventList, row)

	print "Completed execution of instructions for order book!"
	print askTree
	print bidTree


	# For testing only!
	# print "TESTING"
	# details = [1,1,"hi","nicholas","testing"]
	# details2 = [2,1,"hi","nicholas","testing"]
	# print details
	# askTree.add(details)
	# askTree.add(details2)
	# bidTree.add(details)
	# print "Finished adding"
	# time.sleep(2)
	# askTree.remove(1)
	# bidTree.remove(1)


'''
DESCRIPTION:
	This function will define the thread that is responsible for matching transactions with one another

	It will create an instance of TransactionMatcher and runMatches
	
'''
def matchTransactions(askTree, bidTree, databaseQueue, terminateFlag, verbose = False):
	matcher = TransactionMatcher.TransactionMatcher(askTree, bidTree, databaseQueue, terminateFlag, verbose)
	matcher.runMatches()

'''
DESCRIPTION:
	This function will print out a message detailing the use of this program
'''
def usage():
	print "****************USAGE*****************\nArguments are passed to this program via a flag and argument, and settings are set by toggling the flags available.\n\nThis program supports the following flags:\n	-h/--help\n 	-i/--input\n	-o/--output"

def terminateSequence(terminateFlag=None):
	print "Terminating Program ... Killing all threads"
	if terminateFlag is not None:
		terminateFlag.set()


'''
DESCRIPTION:
	This is the main function from which the program will execute from

	It will read in commands passed to it via the command line in the form of a csv file
		The commands in the CSV file should be in the form of "<Ask/Bid>, <Event Details> " 

	It will Start the thread for UI to be displayed (Display.py)

	It will start the thread for the commands for the order book to be fufilled

	It will start the thread that will scan the trees for any match up in orders
'''
if __name__ == '__main__':
	
	# Initialising variables
	databaseQueue = multiprocessing.Queue(maxsize=0)
	askTree = Tree.Tree(1, databaseQueue)
	bidTree = Tree.Tree(0, databaseQueue)
	eventList = EventList.EventList()

	# Read in input from the command line
	inputFile = None
	outputFile = None
	saveOutput = False
	showDisplay = False
	verbose = False

	argv = sys.argv[1:]
	try:
		# opts is a list of arguments e.g. (("-h"), ("-i","test.csv) , ("--output",))
		opts, args = getopt.getopt(argv, "hi:o:sdv", ["help", "inputFile=", "outputFile=", "saveOutput", "display","verbose"] )
	except getopt.GetoptError as e:
		print str(e)
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-i", "--inputFile"):
			inputFile = arg
		elif opt in ("-o", "--outputFile"):
			outputFile = arg
		elif opt in ("-s", "--saveOutput"):
			saveOutput = True
		elif opt in ("-d", "--display"):
			showDisplay = True
		elif opt in ("-v", "--verbose"):
			verbose = True
		else:
			print "This should not happen!"
			assert False, "unhandled option"

	# Complete populating relevant information from csv file
	updateTrees(askTree, bidTree, inputFile, outputFile, saveOutput)

	terminateFlag = threading.Event()
	# Define the thread that will display UI
	if showDisplay:
		displayThread = Thread(target = display, args=(askTree, bidTree, eventList, terminateFlag))
	# Define the thread that will match up orders
	matchingThread = Thread(target=matchTransactions, args=(askTree, bidTree, databaseQueue, terminateFlag, verbose, ))

	# Start the different threads
	
	if showDisplay:
		displayThread.start()

	matchingThread.start()

	# orderBookThread.start()

	# Define some constants to do error checking with the user input for new events
	numAttributes = 5

	# Read in user inputs to add/cancel ask/bid orders
	try:
		while 1:
			if terminateFlag.isSet():
				terminateSequence(terminateFlag)
				break
			print "Enter new event in format 'UserID,Time,Price,NumShares,Type'"
			newEvent = None
			rawNewEvent = raw_input(">")
			if rawNewEvent.lower() in ("stop","quit","exit"):
				terminateSequence(terminateFlag)
				break
			newEvent = [i.strip() for i in rawNewEvent.split(",")]
			# Data filtering to makes sure that the new input is in the right format
			if len(newEvent) != numAttributes:
				print "Wrong Format!"
				continue
			updateTrees(askTree, bidTree, newEvent=newEvent)

	except KeyboardInterrupt as identifier:
		terminateSequence(terminateFlag)
