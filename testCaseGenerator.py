import csv, random, time

sampleSize = 40
listOfUserID = random.sample(range(0,100), sampleSize)
listOfTimeStamps = random.sample(range(int(time.time())-50,int(time.time()+50)), sampleSize)
listOfAskPrices = random.sample(range(5,105), sampleSize/2)
listOfBidPrices = random.sample(range(20,200), sampleSize/2)
listOfNumShares = random.sample(range(1,1000), sampleSize)
# Row should be in format [UserID, Time, Price, NumShares, Type]
with open("selfGenTest.csv", "wb") as csvfile:
    writer = csv.writer(csvfile)
    for i in xrange(sampleSize/2):
        row = [listOfUserID[i], listOfTimeStamps[i], listOfAskPrices[i], listOfNumShares[i], "ask"]
        writer.writerows([row])
    for i in xrange(sampleSize/2,sampleSize):
        row = [listOfUserID[i], listOfTimeStamps[i], listOfBidPrices[i-(sampleSize/2)], listOfNumShares[i], "bid"]
        writer.writerows([row])