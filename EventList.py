from __future__ import print_function
from Queue import *

class Event(object):

	def __init__(self, details_array):
		#details array should be of size ?
		#array indices:
		# 0: userID
		# 1: timestamp
		# 2: numshares
		# 3: price
		self.userID = details_array[0]
		self.timestamp = details_array[1]
		self.numShares = details_array[2]
		self.price = details_array[3]


class EventList(object):

	def __init__(self):
		self.eventDict = {} 		#dictionary
		self.unusedKeys = Queue() 	#queue


	def add(self, event):
		#determine key value
		if(self.unusedKeys.empty()):
			key = len(self.eventDict)
		else:
			key = self.unusedKeys.get()

		#add into dictionary
		self.eventDict[key] = event

		#returns key, price, # shares
		#ret_vals = [key, event.price, event.numShares]
		return(key, event.price, event.numShares)


	def delete(self, event_key):
		del self.eventDict[event_key]
		self.unusedKeys.put(event_key)


	#removes all events after x amount of time
	def flush_events(self):
		pass