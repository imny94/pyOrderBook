from bintrees import FastRBTree
import Queue, copy
import numpy as np

class Tree():

	'''
	DESCRIPTION:
		Initializes:
			Tree Struture which will be used to store information in the tree
			Shares volume to track number of shares traded in Exchange
			Price Map to find Nodes stored in binary tree quickly
			Min price of Exchange
			Max price of Exchange
			Top 10 prices for display
			Types of tree: 0 for bid tree
						   1 for ask tree.

	'''
	def __init__(self,type_of_tree, databaseQueue):
		self.price_tree = FastRBTree()
		self.volume = 0
		self.min_price = None
		self.max_price = None
		self.maxNumNodes = 20#100000
		# Allow for 20% deviation
		self.hardLimit = self.maxNumNodes * 1.2
		self.databaseQueue = databaseQueue
		self.amtToPrune = 2
		self.minSizeOfTree = 3
		self.first10prices=[] # fast to store in list, but need to sort everytime
		self.tree_type = type_of_tree 

	def sizeOfTree(self):
		return len(self.price_tree)

	'''
	DESCRIPTION:
		Adds Node Object to tree if Node is not already on Tree, and if current Tree size is not exceeded
		If Node is already present, update relevant Node 

	ARGUMENTS:
		details - [UserID, Time, Price, NumShares, Type]
	'''
	def add(self, details):
		# print details
		# print "Adding!"
		price = float(details[2])
		numShares = int(details[3])
		self.volume += numShares
		########################NESTED FUNCTION################################
		def updateToTree():
			node = self.lookup(price)
			if node is None:
				# print "New node!"
				# Add node to tree
				newNode = Node(price, details)
				self.price_tree.insert(price, newNode)

			else:
				# print "Exisiting node!"
				# Node exists! Add new order Index to Queue in the respective price node
				node.addKey(details)

			self.updateMaxAndMinPrices(price)

			# check to add prices for display:
			if len(self.first10prices) < 10:
				self.first10prices.append(price)
				self.first10prices.sort()
			# add price if in top 10 range
			if self.tree_type == 0: #bid tree
				if price >= self.first10prices[0]:
					if price not in self.first10prices:
						self.first10prices.pop(0)
						self.first10prices.insert(0,price)
						self.first10prices.sort()
			else:
				if price >= self.first10prices[-1]:
					if price not in self.first10prices:
						self.first10prices.pop(-1)
						self.first10prices.insert(-1,price)
						self.first10prices.sort()
		#####################END OF NESTED FUNCTION#############################

		# Define 2 states for the adding of new nodes, one when the tree's depth limit has been reached, and another otherwise
		if self.sizeOfTree() < self.maxNumNodes:
			# Limit has not been reached, continue adding nodes to tree
			updateToTree()
		else:
			# Tree limit has been reached, need to start deciding which data to keep in tree and DB

			# Different logic for bid and ask tree - bid tree keeps highest prices, ask tree keeps lowest prices
			# 0 - bidTree, 1 - askTree
			if self.tree_type == 1:
				# askTree - Keep minimum prices
				if price > self.getLargestPrice():
					# Add to database
					self.sendRequestToDatabase(details)
				else:
					# Add this event to the node, but we move the bottom x events into the DB if hard limit is reached
					updateToTree()

					if self.sizeOfTree() > self.hardLimit:	
						# Hard Limit has been reached, start pruning tree
						# Function call to add the bottom x number of events into the DB
						for i in xrange(self.amtToPrune):
							nodeToRemove = self.removeNode(self.getLargestPrice())
							event = nodeToRemove.getNextEvent()
							while event is not None:
								self.sendRequestToDatabase(event)
								event = nodeToRemove.getNextEvent()
			elif self.tree_type == 0:
				# bidTree - Keep maximum prices
				if price < self.getSmallestPrice():
					# Add to database
					self.sendRequestToDatabase(details)
				else:
					# Add this event to the node, but we move the bottom x events into the DB if hard limit is reached
					updateToTree()

					if self.sizeOfTree() > self.hardLimit:	
						# Hard Limit has been reached, start pruning tree
						# Function call to add the bottom x number of events into the DB
						for i in xrange(self.amtToPrune):
							nodeToRemove = self.removeNode(self.getSmallestPrice())
							event = nodeToRemove.getNextEvent()
							while event is not None:
								self.sendRequestToDatabase(event)
								event = nodeToRemove.getNextEvent()
			else:
				assert False, "Invalid type!"




	'''
	DESCRIPTION:
		Updates the min and max prices recorded on the tree based on the given price
		Update the weighted average price on the market

	ARGUMENTS:
		price - used to compare with current max and min price and update their values
	'''
	def updateMaxAndMinPrices(self, price):
		if self.max_price == None or self.max_price < price:
			self.max_price = price
		if self.min_price == None or self.min_price > price:
			self.min_price = price

	'''
	DESCRIPTION:
		Removes the given price node from the tree
	RETURNS:
		Returns the removed node if it is required
	'''
	def removeNode(self, price):
		node = self.price_tree.pop(price)
		self.volume -= int(node.numShares)
		# -------------------this is used for display---------------
		# this is for display purpose
		# if self.tree_type==0: #bid tree
		# 	if price >= self.first10prices[0]:
		# 		if price in self.first10prices:
		# 			self.first10prices.remove(price)
		# 			self.first10prices.sort()
		# else:# ask tree
		# 	if price >= self.first10prices[-1]:
		# 		if price in self.first10prices:
		# 			self.first10prices.remove(price)
		# 			self.first10prices.sort()

		if self.tree_type == 0:
			# Bid Tree
			if price in self.first10prices:
				self.first10prices.remove(price)
				#TODO: Implement logic to repopulate first10prices after removing a given entry
		else:
			# Ask Tree
			if price in self.first10prices:
				self.first10prices.remove(price)
				#TODO: Implement logic to repopulate first10prices after removing a given entry

		return node

	'''
	DESCRIPTION:
		This function is used to remove orders from the given price node 
			i.e. Cancelling of orders etc
	'''
	def removeOrderFromNode(self, price, event):
		node = self.lookup(price)
		if node is not None:
			node.removeEvent(event)
		else:
			# Given event is not in tree, might be in database...
			self.sendRequestToDatabase(event)
			


	'''
	DESCRIPTION:
		Searches the Tree for any nodes with the given price
		Returns the reference to Node if node is found, else return None
	'''
	def lookup(self, price):
		if price in self.price_tree:
			return self.price_tree[price]
		return None

	'''
	DESCRIPTION:
		This function will return if the Price Tree is empty or not
	'''
	def isEmpty(self):
		return self.price_tree.is_empty()

	'''
	DESCRIPTION:
		This function will return the largest value on the Tree
	'''
	def getLargestPrice(self):
		return self.price_tree.max_key() if not self.isEmpty() else None

	'''
	DESCRIPTION:
		This function will return the smallest value on the Tree
	'''
	def getSmallestPrice(self):
		return self.price_tree.min_key() if not self.isEmpty() else None

	'''
	DESCRIPTION:
		This function will be used to scan the tree to see if there are any nodes with prices greater than given price.

	RETURNS:
		1) a list of prices greater than the given price if they exist

		2) an Empty List otherwise

	ARGUMENTS:
		price - The price to compare with
		upperBound - Optional argument to set a upper bound on the range to return
	'''
	def hasPriceGreaterThan(self, price, upperBound=float("inf")):
		return [i for i in self.price_tree.key_slice(price,upperBound)] if not self.isEmpty() else None

	'''
	DESCRIPTION:
		This function will be used to scan the tree to see if there are any nodes with prices smaller than given price.

	Returns:
		1) a list of prices greater than the given price if they exist

		2) an Empty List otherwise

	ARGUMENTS:
		price - The price to compare with
		lowerBound - Optional argument to set a lower bound on the range to return
	'''
	def hasPriceSmallerThan(self, price, lowerBound=float('-inf')):
		return [i for i in self.price_tree.key_slice(lowerBound, price)] if not self.isEmpty() else None

	'''
	DESCRIPTION:
		This function will be used to return the oldest event on the respective price node
		While doing so, the queue in the price node should be updated

	RETURNS:
		The oldest event of the respective price node

	ARGUMENTS:
		price - This price is used to identify the given price node to extract the event from
	'''
	def getNextEventForPrice(self, price):
		event = None
		if not self.price_tree.is_empty():
			node = self.price_tree[price]
			event = node.getNextEvent()
		return event

	'''
	DESCRIPTION:
		This function is used to return the number of shares there are in a given node
	'''
	def getNumSharesForPrice(self, price):
		node = self.lookup(price)
		if node is not None:
			return node.getShares()
		return None

	'''
	DESCRIPTION:
		This function is used to return the list of satisfiable order index for a given price node
	'''
	def getSatisfiableOrders(self, price, numShares):
		node = self.lookup(price)
		if node.getShares() == numShares:
			self.removeNode(price)
		return node.getSatisfiableOrders(numShares)
	
	'''
	DESCRIPTION:
		This function is used to send a request for a given event to the Database
		The request might be a request to remove entries in the database, or requests to dump entries into the datbase

	ARGUMENTS:
		event - [EventID, UserID, Time, Price, NumShares, Type]
	'''
	def sendRequestToDatabase(self, event):
		# add event hash to the the event for faster indexing in the database
		event.insert(0,self.__getEventHash(event))
		# insert the event into the database
		self.databaseQueue.put((event[-1].lower(), event))

	'''
	DESCRIPTION:
		This function is used to return a MD5 hash of a given event so it can be added to the queue/ be looked up quickly
	'''
	def __getEventHash(self, event):
		m = hashlib.md5()
		m.update(str(event))
		return m.digest()

	#--------------------These member functions are for display purposes------------------
	def fastDisplay(self):
		'''
		Display top ten prices of the current tree.
		Use numpy array for fast storage.
		Input:
		Output:
			Indexes of the top ten prices.
		'''
		display=np.zeros((10,4))
		if self.tree_type==0: #bid tree
			total=0
			idx=0
			for price in self.first10prices:
				node=self.lookup(price)
				count=node.getNumOrders()
				amount=node.getShares()
				total+=amount
				display[9-idx]=np.array(([count,amount,total,price]))
				idx+=1
		else: # ask tree
			total=0
			idx=0
			for price in self.first10prices:
				node=self.lookup(price)
				count=node.getNumOrders()
				amount=node.getShares()
				total+=amount
				display[idx]=np.array(([price,total,amount,count]))
				idx+=1
		return display




from collections import OrderedDict
import hashlib

class Node():
	'''
	DESCRIPTION:
		Initializes:
			Queue to store record of orders at given price
			Price to represent value of Node

	ARGUMENTS:
		price - The price this node represents
		event - [UserID, Time, Price, NumShares, Type]
	'''
	def __init__(self, price, event):
		# Initialize size of queue to be infinity
		self.orderQueue = OrderedDict()
		#TODO: Add details to the queue
		self.orderQueue[self.__getEventHash(event)] = event
		self.price = price
		self.numShares = int(event[3])

	'''
	DESCRIPTION:
		This function is used to return a MD5 hash of a given event so it can be added to the queue/ be looked up quickly
	'''
	def __getEventHash(self, event):
		m = hashlib.md5()
		m.update(str(event))
		return m.digest()

	'''
	DESCRIPTION:
		This function will serve to update the respective queue on the node with new keys that will reference the data stored in eventlist
		and update the value of numShares

	ARGUMENTS:
		event - [UserID, Time, Price, NumShares, Type]
	'''
	def addKey(self, event):
		self.orderQueue[self.__getEventHash(event)] = event
		self.numShares += int(event[3])

	'''
	DESCRIPTION:
		This function will extract the oldest value on the queue and return it
	'''
	def getNextEvent(self):
		event = None
		if self.getNumOrders() > 0:
			# item here is the key : value pair, so event is in the second index
			key, event = self.orderQueue.popitem(last=False)
			self.numShares -= int(event[3])
		return event

	'''
	DESCRIPTION:
		This function will remove the given index from the orderQueue, and update the value of numShares
	ARGUMENTS:
		index - represents the index of the object to be removed from list
		numShares - The number of shares that corresponds to this index being removed
	'''
	def removeEvent(self, event):
		entry = self.__getEventHash(event)
		if entry in self.orderQueue:
			# newEvent = [UserID, Time, Price, NumShares, Type]
			newEvent = self.orderQueue.pop(entry, None)
			self.numShares -= int(newEvent[3])

	'''
	DESCRIPTION:
		This is used to give the number of orders in the queue for current node
	'''
	def getNumOrders(self):
		return len(self.orderQueue)

	'''
	DESCRIPTION:
		This is used to get the number of shares that is being traded at this current price
	'''
	def getShares(self):
		return self.numShares

	'''
	DESCRIPTION:
		This function is used to get the full orderQueue
	'''
	def getOrderQueue(self):
		return self.orderQueue

	'''
	DESCRIPTION:
		This function will iterate through the list of orders trying to reached the required number of shares as given as a parameter, while removing the order from the queue
		If the number of shares has been met, update the new value of the first item in the queue
	RETURNS:
		A list of orderIndexes that can be satisfied
		NOTE The last item on the list returned should not be directly modified if any changes needs to be made, as it is the pointer which points directly to the event in the node
	'''
	def getSatisfiableOrders(self, sharesToMatch):
		if self.getShares() == sharesToMatch:
			return [i for i in self.orderQueue.values()]
		returnList = []
		iter = self.orderQueue.itervalues()
		# print "Shares to match %d"%sharesToMatch
		while int(sharesToMatch) > 0:
			# Note that the event here is merely a pointer that points to the item in the dictionary, 
			# so changing this value will change values in the dictionary as well
			try:
				event = iter.next()
			except StopIteration:
				break
			orderNumShares = int(event[3])
			if orderNumShares <= sharesToMatch:
				sharesToMatch -= orderNumShares
				self.orderQueue.popitem(last=False)
				returnList.append(event)
				self.numShares -= event[3]
			# Demand has been satisfied, update the value of the first item in the queue after satisfing demand
			else:
				# Update the value of the first item on the queue
				newNumShares = orderNumShares-sharesToMatch
				newEvent = copy.deepcopy(event)
				event[3] = int(newNumShares)
				newEvent[3] = sharesToMatch
				returnList.append(newEvent)
				#NOTE: This might be a cause some issues as we are returning a pointer to event, which might cause event to inadvertently be editted...
				sharesToMatch -= orderNumShares
				self.numShares -= newEvent[3]
		return returnList



def main():
	t = Tree()
	t.add([1,2,3,4,5])
	t.add([2,3,4,5,6])
	t.add([3,4,5,6,7])
	t.add([1,7,3,4,5])
	t.add([2,6,4,5,6])
	t.add([3,5,5,6,7])
	t.add([1,11,3,4,5])
	t.add([2,51,4,5,6])
	t.add([3,78,5,6,7])
	t.add([1,46,3,4,5])
	t.add([2,33,4,5,6])
	t.add([3,22,5,6,7])
	print t.hasPriceGreaterThan(10)
	print t.hasPriceSmallerThan(100)
	print t.getOrderIndexForPrice(22)

if __name__ == '__main__':
	main()
