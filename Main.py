import sys, getopt, csv, time
from threading import Thread

import Tree
import EventList

'''
DESCRIPTION:
	This function will contain all the method calls required to run the UI on a separate thread
'''
def display(askTree, bidTree, eventList):
	print "Display!"
	while 1:
		askTree.display()
		bidTree.display()
		time.sleep(1)
	pass


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
def orderBook(askTree, bidTree, eventList, inputFile, outputFile = None, saveOutput = False):

	if inputFile == None:
		assert False, "No input file for commands given!"

	if saveOutput:
		if outputFile == None:
			assert False, "No output file specified!"

	# Read in the csv file
	with open(inputFile, "rb") as csvfile:
		reader = csv.reader(csvfile)
		# Row should be in format [Ask/Bid>,<Event Details>]
		for row in reader:
			# Add the given events into the eventlist
			detailsForNode = eventList.add(EventList.Event(row[1:]))
			# e.g of detailsForNode = (1, 'price2', 'shares2')

			AorB = row[0]
			if AorB == "Ask":
				askTree.add(detailsForNode)
			elif AorB == "Bid":
				bidTree.add(detailsForNode)
			else:
				assert False, "Invalid command: %s given!"%row

	print "Completed execution of instructions for order book!"

	# For testing only!
	print "TESTING"
	details = [1,1,"hi","nicholas","testing"]
	details2 = [2,1,"hi","nicholas","testing"]
	print details
	askTree.add(details)
	askTree.add(details2)
	bidTree.add(details)
	print "Finished adding"
	time.sleep(2)
	askTree.remove(1)
	bidTree.remove(1)


'''
DESCRIPTION:
	This function will define the thread that is responsible for matching transactions with one another
'''
def matchTransactions(askTree, bidTree, eventList):
	print "Matching Transactions!"
	pass

'''
DESCRIPTION:
	This function will print out a message detailing the use of this program
'''
def usage():
	print "****************USAGE*****************\nArguments are passed to this program via a flag and argument, and settings are set by toggling the flags available.\n\nThis program supports the following flags:\n	-h/--help\n 	-i/--input\n	-o/--output"

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
	askTree = Tree.Tree()
	bidTree = Tree.Tree()
	eventList = EventList.EventList()

	# Read in input from the command line
	inputFile = None
	outputFile = None
	saveOutput = False

	argv = sys.argv[1:]
	try:
		# opts is a list of arguments e.g. (("-h"), ("-i","test.csv) , ("--output",))
		opts, args = getopt.getopt(argv, "hi:os", ["help", "input=", "output=", "saveOutput"] )
	except getopt.GetoptError as e:
		print str(e)
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-i", "--input"):
			inputFile = arg
		elif opt in ("-o", "--output"):
			outputFile = arg
		elif opt in ("-s", "--saveOutput"):
			saveOutput = True
		else:
			print "This should not happen!"
			assert False, "unhandled option"

	# Define the thread that will display UI
	displayThread = Thread(target = display, args=(askTree, bidTree, eventList, ))
	# Define the thread that will maintain order book
	orderBookThread = Thread(target=orderBook, args=(askTree, bidTree, eventList, inputFile, outputFile, saveOutput ))
	# Define the thread that will match up orders
	matchingThread = Thread(target=matchTransactions, args=(askTree, bidTree, eventList))

	# Start the different threads
	displayThread.start()
	orderBookThread.start()
	matchingThread.start()

	print "Completed running all threads"