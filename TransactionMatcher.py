import time
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

class TransactionMatcher():

    def __init__(self, askTree, bidTree, eventList, terminateFlag, verbose):
        self.askTree = askTree
        self.bidTree = bidTree
        self.eventList = eventList
        self.terminateFlag = terminateFlag
        self.verbose = verbose

    def debugLog(self,msg):
        if self.verbose:
            logging.debug(msg)

    '''
    DESCRIPTION:
        The current algorithm implemented will be one that matches the highest bid price to the lowest ask price. (Note that the perspective of the ask and bid price are from the investors POV)

        If there is a match between the asking and bidding prices, the order book will try to match as many of the orders it can for that given price
    '''
    def runMatches(self):
        logging.debug("Matching Transactions!")
        while 1:
            if self.terminateFlag.isSet():
                self.debugLog("Terminating Thread!")
                break
            minAskPrice = self.askTree.getSmallestPrice()
            maxBidPrice = self.bidTree.getLargestPrice()
            # logging.debug("minAskPrice: %s , maxBidPrice: %s"%(minAskPrice,maxBidPrice))

            if minAskPrice is None or maxBidPrice is None:
                self.debugLog("Either the ask tree or bid tree is empty! Waiting for tree to be populated")
                time.sleep(1)
                continue
            
            if maxBidPrice < minAskPrice:
                time.sleep(1)
                continue

            # Transaction is a profitable one!
            numAskingShares = self.askTree.getNumSharesForPrice(minAskPrice)
            numBiddingShares = self.bidTree.getNumSharesForPrice(maxBidPrice)

            # Everything can be sold
            if numAskingShares < numBiddingShares:
                # Remove the price node from the askTree as all the orders in that node has been served
                askNode = self.askTree.removeNode(minAskPrice)
                # Get the order Queue in terms of the orderIndex only. Order queue is a sortedDictionary of events
                askOrders = askNode.getOrderQueue().values()
                # Get the list of orderIndex that can be satisfied
                bidOrders = self.bidTree.getSatisfiableOrders(maxBidPrice, numBiddingShares)

                #TODO: Need to update transaction matcher to continue with logic after a transaction has been matched!

            # There are some remaining shares that remains to be sold
            else:
                # Remove the price node from the bidTree as all the orders in that node has been served
                bidNode = self.bidTree.removeNode(maxBidPrice)
                # Get the order Queue in terms of the orderIndex only. Order queue is a sortedDictionary of events
                bidOrders = bidNode.getOrderQueue().values()
                # Get the list of orderIndex that can be satisfied
                askOrders = self.askTree.getSatisfiableOrders(minAskPrice, numAskingShares)

                #TODO: Need to update transaction matcher to continue with logic after a transaction has been matched!
            logging.debug("Successfully matched Transaction!")
