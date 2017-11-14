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
				This will contain all the details that is to be stored in the node
	'''
	def add(self, details):
		key = details[0]
		price = details[1]
		node = self.lookup(details[1])
		if not node:
			# Add node to tree
			newNode = Node(price, details)
			self.price_tree.insert(price, newNode)
			# Add price into price_map which points directly to respective Node
			self.price_map[price] = newNode
			return
		# Node exists! Update current node with new order
		self.update(node,details)

	'''
	DESCRIPTION:
		Removes the given price node from the tree and price_map
	'''
	def remove(self, price):
		node = self.price_map.pop(price)
		self.price_tree.remove(price)

	'''
	DESCRIPTION:
		Searches the Tree for any nodes with the given price
		Returns the reference to Node if node is found, else return False
	'''
	def lookup(self, price):
		if price in self.price_map:
			return self.price_tree[price]
		return False

	'''
	DESCRIPTION:
		This function will serve to update the respective node with more the respective details
	'''
	def update(self, node, details):
		node.orderQueue.put(details)

class Node():
	'''
	DESCRIPTION:
		Initializes:
			Queue to store record of orders at given price
			Price to represent value of Node

	ARGUMENTS:
		details - (1, 'price2', 'shares2') -> [key, event.price, event.numShares]
				This will contain all the details that is to be stored in the node
	'''
	def __init__(self, price, order):
		# Initialize size of queue to be infinity
		self.orderQueue = Queue.Queue(maxsize=0)
		self.orderQueue.put(order)
		self.price = price

	'''
	DESCRIPTION:
		This is used to give the number of orders in the queue for current node
	'''
	def NumOrders(self):
		return self.orderQueue.qsize()