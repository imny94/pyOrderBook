import time

class TransactionMatcher():

    def __init__(self, askTree, bidTree, eventList):
        self.askTree = askTree
        self.bidTree = bidTree
        self.eventList = eventList

    '''
    DESCRIPTION:
        The current algorithm implemented will be one that matches the highest bid price to the lowest ask price. (Note that the perspective of the ask and bid price are from the investors POV)

        If there is a match between the asking and bidding prices, the order book will try to match as many of the orders it can for that given price
    '''
    def runMatches(self):
        print "Matching Transactions!"
        while 1:
            minAskPrice = self.askTree.getSmallestPrice()
            maxBidPrice = self.bidTree.getLargestPrice()

            if minAskPrice or maxBidPrice is None:
                print "Either the ask tree or bid tree is empty! Waiting for tree to be populated"
                time.sleep(1)
                continue
            
            if maxBidPrice < minAskPrice:
                time.sleep(1)
                continue

            # Transaction is a profitable one!
            numAskingShares = self.askTree.getNumSharesForPrice(minAskPrice)
            numBiddingShares = self.bidTree.getNumSharesForPrice(maxBidPrice)

            # Everything can be sold
            if numAskingShares > numBiddingShares:
                # Remove the price node from the askTree as all the orders in that node has been served
                askNode = self.askTree.remove(minAskPrice)
                # Get the order Queue in terms of the orderIndex only. Note that the orderQueue is a list of Sets, so that data is filtered here
                askOrders = [i[0] for i in askNode.getOrderQueue()]
                # Get the list of orderIndex that can be satisfied
                bidOrders = self.bidTree.getSatisfiableOrders(maxBidPrice, numBiddingShares)
                # Note that the last item in bidOrders is a set that contains the order index to update
                indexToUpdate, newNumShares = bidOrders.pop(-1)

                # # Update the eventlist
                # currentTime = time.time()
                # self.eventList.successTrades(askOrders, minAskPrice, currentTime)
                # self.eventList.successTrades(bidOrders, maxBidPrice, currentTime)
                # self.eventList.tradeAmount(indexToUpdate, maxBidPrice, currentTime, newNumShares)

            # There are some remaining shares that remains to be sold
            else:
                # Remove the price node from the bidTree as all the orders in that node has been served
                bidNode = self.bidTree.remove(maxBidPrice)
                # Get the order Queue in terms of the orderIndex only. Note that the orderQueue is a list of Sets, so that data is filtered here
                bidOrders = [i[0] for i in bidNode.getOrderQueue()]
                # Get the list of orderIndex that can be satisfied
                askOrders = self.askTree.getSatisfiableOrders(minAskPrice, numAskingShares)
                # Note that the last item in bidOrders is a set that contains the order index to update
                indexToUpdate, newNumShares = askOrders.pop(-1)

                # # Update the eventlist
                # currentTime = time.time()
                # self.eventList.successTrades(askOrders, minAskPrice, currentTime)
                # self.eventList.successTrades(bidOrders, maxBidPrice, currentTime)
                # self.eventList.tradeAmount(indexToUpdate, minAskPrice, currentTime, newNumShares)
