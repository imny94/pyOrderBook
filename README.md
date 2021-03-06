# NTU-BitCoin Team 9

This is an implementation of a fast order book that can be used on exchanges for Cryptocurrency such as Bitcoin, Etherium, Bitcoin Cash, etc. 
It uses a depth-limited red-black tree for storage of events in memory, allowing fast matching of transactions and lookups within the Tree. For instances where the number of events becomes too great to be stored entirely in memory, the least relevant events are stored in a SQLite Database, allowing the program to handle large number of transactions without impacting the performance of the order book too drastically.
This program includes a user interface to display the current market price and order books. 

## Setup/Installation

#### Python version: python 2.7.10

#### Packages Dependencies

###### tkinter, PIL, sqlite3, numpy, bintrees

Please run the following command in the command line to get the necessary dependencies.
```
python setup.py
```
It will recognize the Operating System of your system and install the necessary dependencies for this program.

Should the above fail, please install the required packages manually according to your operating system.
#### How to run the program

This program can be run from the command line with the following command:
```
python Main.py
```

Additionally, this program takes in the following flags and arguments:

 Flag | Full Flag | Arguments 
 ---- | :-------: | --------: 
 -i   | --input   | nameOfCSVFile
 -v   | --verbose |           
 -d   | --display |           
 -m   | --maxSize | desiredSize
 
 Use the input -i flag to pre-load transactions for the program from a csv file.
 Use the verbose -v flag to show messages from background threads.
 Use the -d display flag to show a display for the order book.
 Use the -m maxSize flag to set a limit on the size of the ask and bid tree, if unspecified, default is 100000
 
 E.g.
 ```
 python Main.py -i test.csv -v -d
 ```

#### Dynamic addition of transactions to the program

When the program is running, transactions can be passed to the program dynamically through the command line.
Enter the new transaction into the command line in the following format:

UserID,Time,Price,Number of Shares,Type

NOTE: Type only accepts the following 4 types : "ask", "bid", "cask", "cbid"
where "cask" and "cbid" represents cancel events for ask and bid events

E.g.
6542316, 3244657, 500.00, 50, ask

## Importing of the OrderBook as a package

This orderbook can be imported as a package as a part of a larger program. 

To create an instance of this order book in python, import the file OrderBook, and create an instance of the class defined inside OrderBook.

E.g.
```
import OrderBook as OrderBook
import multiprocessing

inputQueue = multiprocessing.Queue()
instance = OrderBook(inputQueue)
instance.run()
```

Refer to file: SampleCode.py for more detailed information/examples/comments on how to use this program as a package.

## Team Members:

This project was done as a part of a course, Bitcoin in the Big Data Era during the fall of 2017 at National Taiwan University, with collaborations between exchange and local students in National Taiwan University coming from different disciplines and backgrounds. The members of the team are as follows:

[Nicholas Yeow](https://github.com/imny94) [T06902106] - Singapore University of Technology and Design

[Tan Kwan Fu](https://github.com/wilfred55555) [T06501101] - Singapore University of Technology and Design

[Angela Yung](https://github.com/asyung) [T06902101] - University of California, Santa Barbara

[Yifan Li](https://github.com/brucefeynman) [T06901110] - Jilin University (吉林大学）

Deniz Sen [T06303125] - Leiden university

Yao-Cheng Zhang [B04902047] - National Taiwan University (国立台湾大学）
