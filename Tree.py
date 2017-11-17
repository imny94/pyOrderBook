from bintrees import FastRBTree
import Queue
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
	def __init__(self,type_of_tree):
		self.price_tree = FastRBTree()
		self.volume = 0
		self.min_price = None
		self.max_price = None
		self.first10prices=[] # fast to store in list, but need to sort everytime
		self.tree_type = type_of_tree 

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
		self.volume += int(numShares)
		node = self.lookup(details[1])
		if node == None:
			print "New node!"
			# Add node to tree
			newNode = Node(price, key, numShares)
			self.price_tree.insert(price, newNode)

		else:
			print "Exisiting node!"
			# Node exists! Add new order Index to Queue in the respective price node
			node.addKey(key, numShares)

		self.updateMaxAndMinPrices(price)

		# check to add prices for display:
		if len(self.first10prices) < 10:
			self.first10prices.append(price)
			self.first10prices.sort()
		# add price if in top 10 range
		if self.tree_type==0: #bid tree
			if price >= self.first10prices[0]:
				if price not in self.first10prices:
					self.first10prices.pop[0]
					self.first10prices.insert(0,price)
					self.first10prices.sort()
		else:
			if price >= self.first10prices[-1]:
				if price not in self.first10prices:
					self.first10prices.pop[-1]
					self.first10prices.insert(-1,price)
					self.first10prices.sort()



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
	'''
	def remove(self, price):
		node = self.price_tree.get(price)
		self.volume -= node.numShares

	'''
	DESCRIPTION:
		This function is used to remove orders from the given price node 
			i.e. Cancelling of orders etc
	'''
	def removeOrderFromNode(self, price, orderIndex, numShares):
		node = self.price_tree.get(price)
		node.removeKey(orderIndex, numShares)


	'''
	DESCRIPTION:
		Searches the Tree for any nodes with the given price
		Returns the reference to Node if node is found, else return False
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

	Returns:
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
		This function will be used to return the oldest order index on the respective price node
		While doing so, the queue in the price node should be updated

	RETURNS:
		The oldest order Index of the respective price node

	ARGUMENTS:
		price - This price is used to identify the given price node to extract the order index from
	'''
	def getOrderIndexForPrice(self, price):
		orderIndex = None
		if not self.price_tree.is_empty():
			node = self.price_tree[price]
			orderIndex = node.getOrderIndex()
		return orderIndex

	'''
	DESCRIPTION:
		This function is used to return the number of shares there are in a given node
	'''
	def getNumSharesForPrice(self, price):
		node = self.lookup(price)
		if node is not None:
			return node.getShares()
		return None

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
				display[idx]=np.array(([price,toal,amount,count]))
				idx+=1
		return display






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
		self.orderQueue = []
		self.orderQueue.append((orderIndex, numShares))
		self.price = price
		self.numShares = numShares

	'''
	DESCRIPTION:
		This function will serve to update the respective queue on the node with new keys that will reference the data stored in eventlist
		and update the value of numShares
	'''
	def addKey(self, key, numShares):
		self.orderQueue.append((key, numShares))
		self.numShares += numShares

	'''
	DESCRIPTION:
		This function will extract the oldest value on the queue and return it
	'''
	def getOrderIndex(self):
		if self.getNumOrders() > 0:
			orderIndex, orderNumShares = self.orderQueue.pop(0)
			self.numShares -= orderNumShares
		else:
			orderIndex = None
		return orderIndex

	'''
	DESCRIPTION:
		This function will remove the given index from the orderQueue, and update the value of numShares
	ARGUMENTS:
		index - represents the index of the object to be removed from list
		numShares - The number of shares that corresponds to this index being removed
	'''
	def removeKey(self, key, numShares):
		entry = (key, numShares)
		if entry in self.orderQueue:
			self.orderQueue.remove(entry)
			self.numShares -= numShares

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