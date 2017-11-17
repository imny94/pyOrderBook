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
            maxiBidPrice = self.bidTree.getLargestPrice()
            
            if maxiBidPrice < minAskPrice:
                time.sleep(1)
                break

            # Transaction is a profitable one!
            numAskingShares = self.askTree.getNumSharesForPrice(minAskPrice)
            numBiddingShares = self.bidTree.getNumSharesForPrice(maxiBidPrice)

            # Everything can be sold
            if numAskingShares > numBiddingShares:
                # Remove the price node from the askTree as all the orders in that node has been served
                askNode = self.askTree.remove(minAskPrice)
                # Get the order Queue in terms of the orderIndex only. Note that the orderQueue is a list of Sets, so that data is filtered here
                askOrders = [i[0] for i in askNode.getOrderQueue()]
                # Get the list of orderIndex that can be satisfied
                bidOrders = self.bidTree.getSatisfiableOrders(maxiBidPrice, numBiddingShares)
                # Note that the last item in bidOrders is a set that contains the order index to update
                indexToUpdate, newNumShares = bidOrders.pop(-1)

                # Update the eventlist
                self.eventList.
                pass

            # There are some remaining shares that remains to be sold
            else:
                
                pass
