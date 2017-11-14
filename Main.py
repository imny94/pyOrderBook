import sys, getopt, csv, time
from multiprocessing import Process
from threading import Thread
from multiprocessing.managers import BaseManager

import Tree
import EventList

'''
DESCRIPTION:
	This function will contain all the method calls required to run the UI on a separate process
'''
def display(askTree, bidTree, eventList):
	print "Display!"
	# while 1:
	# 	askTree.display()
	# 	bidTree.display()
	# 	time.sleep(1)
	pass


'''
DESCRIPTION:

	This function will initialise the required variables
		- The different binary trees that will be used to store the prices for different bidding price/asking price, along with the relevant transactions poised to happen for that given price
			- Ask Tree
			- Bid Tree
		- The EventList that will be used to record and store events

	It will read in commands passed to it via the command line in the form of a csv file and execute the commands in order
		The commands in the CSV file should be in the form of "<Ask/Bid>, <Event Details> " 
		Running the commands comprises of :
			Inserting event into EventList
			Updating of different Trees

ARGUMENTS:
	argv - command line arguments will be passed via this variable
		+ This is a list of arguments e.g. ["-h", "-i", "smt.csv"]
		+ argv only supports reading in an input csv file, and another output file
'''
def orderBook(argv, askTree, bidTree, eventList):

	# Read in input from the command line
	try:
		opts, args = getopt.getopt(argv, "hi:os", ["help", "input=", "output=", "saveOutput"] )
	except getopt.GetoptError as e:
		print str(e)
		usage()
		sys.exit(2)
	inputFile = None
	outputFile = None
	saveOutput = False
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
	# print "TESTING"
	# node = Tree.Node(["hi","nicholas","testing"])
	# print node
	# askTree.add(node)
	# bidTree.add(node)
	# print "Finished adding"
	# time.sleep(2)
	# askTree.remove(node)
	# bidTree.remove(node)


'''
DESCRIPTION:
	This function will define the process that is responsible for matching transactions with one another
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

	It will Start the process for UI to be displayed (Display.py)

	It will start the process for the commands for the order book to be fufilled

	It will start the process that will scan the trees for any match up in orders
'''
if __name__ == '__main__':
	
	# Initialising variables
	askTree = Tree.Tree()
	bidTree = Tree.Tree()
	eventList = EventList.EventList()

	# Define the thread that will display UI
	displayThread = Thread(target = display, args=(askTree, bidTree, eventList, ))
	# Define the thread that will maintain order book
	orderBookThread = Thread(target=orderBook, args=(sys.argv[1:], askTree, bidTree, eventList, ))
	# Define the thread that will match up orders
	matchingThread = Thread(target=matchTransactions, args=(askTree, bidTree, eventList))

	# Start the different processes
	displayThread.start()
	orderBookThread.start()
	matchingThread.start()

	print "Completed running all processes"