import time
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

class TransactionMatcher():

    def __init__(self, askTree, bidTree, databaseQueue, terminateFlag, verbose):
        self.askTree = askTree
        self.bidTree = bidTree
        self.databaseQueue = databaseQueue
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
        self.debugLog("Matching Transactions!")
        while 1:
            if self.terminateFlag.isSet():
                self.debugLog("Terminating Thread!")
                break
            minAskPrice = self.askTree.getSmallestPrice()
            maxBidPrice = self.bidTree.getLargestPrice()
            # logging.debug("minAskPrice: %s , maxBidPrice: %s"%(minAskPrice,maxBidPrice))

            if minAskPrice is None or maxBidPrice is None:
                # self.debugLog("Either the ask tree or bid tree is empty! Waiting for tree to be populated")
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
                bidOrders = self.bidTree.getSatisfiableOrders(maxBidPrice, numAskingShares)

                #TODO: Need to update transaction matcher to continue with logic after a transaction has been matched!
            elif numAskingShares == numBiddingShares:
                askNode = self.askTree.removeNode(minAskPrice)
                bidNode = self.bidTree.removeNode(maxBidPrice)

                askOrders = askNode.getOrderQueue().values()
                bidOrders = bidNode.getOrderQueue().values()
            # There are some remaining shares that remains to be sold
            else:
                # Remove the price node from the bidTree as all the orders in that node has been served
                bidNode = self.bidTree.removeNode(maxBidPrice)
                # Get the order Queue in terms of the orderIndex only. Order queue is a sortedDictionary of events
                bidOrders = bidNode.getOrderQueue().values()
                # Get the list of orderIndex that can be satisfied
                askOrders = self.askTree.getSatisfiableOrders(minAskPrice, numBiddingShares)

            #TODO: Need to update transaction matcher to continue with logic after a transaction has been matched!
            #BidOrders and AskOrders are both lists of events
            #need to start making transactions
            self.debugLog("Successfully matched Transaction!")
            #index of numShares: 3
            while askOrders and bidOrders:
                remainder = float(askOrders[0][3]) - float(bidOrders[0][3])
                if remainder > 0:
                    #edit ask
                    askOrders[0][3] = remainder

                    #create AskEvent with updated numShares
                    newAskEvent = askOrders[0]
                    newAskEvent[3] = float(bidOrders[0][3])

                    newBidEvent = bidOrders.pop(0)
                if remainder < 0: #there are more bidOrders than askOrders
                    #edit bid
                    bidOrders[0][3] = 0 - remainder #makes the numShares positive

                    newBidEvent = bidOrders[0]
                    newBidEvent[3] = float(askOrders[0][3])

                    newAskEvent = askOrders.pop(0)
                else:
                    newAskEvent = askOrders.pop(0)
                    newBidEvent = bidOrders.pop(0)

                newTransaction = self.createTransaction(newAskEvent, newBidEvent)
                self.databaseQueue.put(("transactions",newTransaction))


    def createTransaction(self, askEvent, bidEvent):
        #index 0: userId
        #index 2: price
        #index 3: numShares
        totalProfit = int(askEvent[3]) * (float(bidEvent[2]) - float(askEvent[2]))
        tradePrice  = float(bidEvent[2])
        tradeEvent  = [askEvent[0], bidEvent[0], str(datetime.now()), tradePrice, askEvent[3], totalProfit, 2]
        return tradeEvent
