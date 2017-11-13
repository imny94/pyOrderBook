import sys, getopt, csv

import Tree
import EventList

'''
DESCRIPTION:
	This function will contain all the method calls required to run the UI on a separate process
'''
def display():
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
def orderBook(argv):

	# Initialising variables
	askTree = Tree.Tree()
	bidTree = Tree.Tree()
	eventList = EventList.EventList()

	# Read in input from the command line
	try:
		opts, args = getopt.getopt(argv, "hi:os", ["help", "csvInput=", "csvOutput=", "saveOutput"] )
	except getopt.GetoptError as e:
		print str(e)
		usage()
		sys.exit(2)
	csvInput = None
	csvOutput = None
	saveOutput = False
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-i", "--csvInput"):
			csvInput = arg
		elif opt in ("-o", "--csvOutput"):
			csvOutput = arg
		elif opt in ("-s", "--saveOutput"):
			saveOutput = True
		else:
			print "This should not happen!"
			assert False, "unhandled option"

	if csvInput == None:
		assert False, "No input file for commands given!"

	if saveOutput:
		if csvOutput == None:
			assert False, "No output file specified!"

	# Read in the csv file
	with open(csvInput, "rb") as csvfile:
		reader = csv.reader(csvfile)
		# Row should be in format [Ask/Bid>,<Event Details>]
		for row in reader:
			AorB = row[0]
			if AorB == "Ask":
				askTree.add(Tree.Node(row[1:]))
			elif AorB == "Bid":
				bidTree.add(Tree.Node(row[1:]))
			else:
				assert False, "Invalid command: %s given!"%row

			# Add the given events into the eventlist
			eventList.add(EventList.Event(row[1:]))


'''
DESCRIPTION:
	This is the main function from which the program will execute from

	It will Start the process for UI to be displayed (Display.py)

	It will start the process for the commands for the order book to be fufilled

	It will start the process that will scan the trees for any match up in orders
'''
if __name__ == '__main__':
	orderBook(sys.argv[1:])