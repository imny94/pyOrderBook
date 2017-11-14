from bintrees import FastRBTree
import Queue

class Tree():

	'''
	DESCRIPTION:
		Initializes:
			Tree Struture which will be used to store information in the tree
			Shares volume to track number of shares traded in Exchange
			Price Map to find Nodes stored in binary tree quickly
			Min price of Exchange
			Max price of Exchange

	'''
	def __init__(self):
		self.price_tree = FastRBTree()
		self.volume = 0
		self.price_map = {}
		self.min_price = None
		self.max_price = None

	'''
	DESCRIPTION:
		Adds Node Object to tree if Node is not already on Tree, and if current Tree size is not exceeded
		If Node is already present, update relevant Node 

	ARGUMENTS:
		details - (1, 'price2', 'shares2') -> [key, event.price, event.numShares]
				This will contain the relevant details that is to be stored in the node
	'''
	def add(self, details):
		print "Adding!"
		key = details[0]
		price = details[1]
		numShares = details[2]
		self.volume += numShares
		node = self.lookup(details[1])
		if node == None:
			print "New node!"
			# Add node to tree
			newNode = Node(price, key)
			self.price_tree.insert(price, newNode, numShares)
			# Add price into price_map which points directly to respective Node
			self.price_map[price] = newNode
		else:
			print "Exisiting node!"
			# Node exists! Add new order Index to Queue in the respective price node
			node.addKey(key, numShares)

		self.updateMaxAndMinPrices(price)

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
		Removes the given price node from the tree and price_map
	'''
	def remove(self, price):
		node = self.price_map.pop(price)
		self.volume -= node.numShares
		self.price_tree.remove(price)

	'''
	DESCRIPTION:
		Searches the Tree for any nodes with the given price
		Returns the reference to Node if node is found, else return False
	'''
	def lookup(self, price):
		if price in self.price_map:
			return self.price_tree[price]
		return None

	'''
	DESCRIPTION:
		This function will be used to scan the tree to see if there are any nodes with prices greater than given price.

	Returns:
		1) a list of prices greater than the given price if they exist

		2) an Empty List otherwise

	ARGUMENTS:
		price - The price to compare with
	'''
	def hasPriceGreaterThan(self, price):
		pass

	'''
	DESCRIPTION:
		This function will be used to scan the tree to see if there are any nodes with prices smaller than given price.

	Returns:
		1) a list of prices greater than the given price if they exist

		2) an Empty List otherwise

	ARGUMENTS:
		price - The price to compare with
	'''
	def hasPriceSmallerThan(self, price):
		pass

	'''
	DESCRIPTION:
		This function will be used to return the oldest order index on the respective price node
		While doing so, the queue in the price node should be updated

	RETURNS:
		The oldest order Index of the respective price node

	ARGUMENTS:
		price - This price is used to identify the given price node to extract the order index from
	'''
	def getOrderIndexForPrice(self, price):
		pass



class Node():
	'''
	DESCRIPTION:
		Initializes:
			Queue to store record of orders at given price
			Price to represent value of Node

	ARGUMENTS:
		price - The price this node represents
		orderIndex - The index of a given event as stored in eventList
	'''
	def __init__(self, price, orderIndex, numShares):
		# Initialize size of queue to be infinity
		self.orderQueue = Queue.Queue(maxsize=0)
		self.orderQueue.put(orderIndex)
		self.price = price
		self.numShares = numShares

	'''
	DESCRIPTION:
		This function will serve to update the respective queue on the node with new keys that will reference the data stored in eventlist
	'''
	def addKey(self, key, numShares):
		self.orderQueue.put(key)
		self.numShares += numShares

	'''
	DESCRIPTION:
		This is used to give the number of orders in the queue for current node
	'''
	def NumOrders(self):
		return self.orderQueue.qsize()