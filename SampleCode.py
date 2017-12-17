import multiprocessing, time
# Import OrderBook Class
from OrderBook import OrderBook

# Initialise a Queue to pass new transactions to the orderbook
inputQueue = multiprocessing.Queue(maxsize=0)
# Initialise an instance of the order book
test = OrderBook(inputQueue, verbose=True)
# Start the order book
test.run()
'''
Entries to inputQueue should be of the following format: [UserID, Time, Price, NumShares, Type]

There is no constraint on what kind of data is given for UserID and Time

However, Price and NumShares should both be numerical values

Type can only take in the following 4 types: "ask", "bid", "cask" and "cbid"
    "cbid" and "cask" are to cancel bid and ask orders respectively
'''
# Examples of how to add entries onto the InputQueue for orderbook
inputQueue.put([1231241, 1231, 4654, 987987, "ask" ])
inputQueue.put([14, 1231, 4134654, 124331, "ask" ])
inputQueue.put([1231241, 1231, 5225, 987987, "bid" ])
inputQueue.put([14, 1231, 41342525654, 124331, "bid" ])
inputQueue.put([1231241, 1231, 4654, 987987, "cask" ])
inputQueue.put([14, 1231, 41342525654, 124331, "cbid"])

time.sleep(10)
# Example of how to terminate the orderbook gracefully
test.terminate()

