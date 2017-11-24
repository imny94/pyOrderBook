# NTU-BitCoin Team 9

This is an implementation of a fast order book that can be used on exchanges for Cryptocurrency such as Bitcoin, Etherium, Bitcoin Cash, etc. 
It uses a depth-limited red-black tree for storage of events in memory, allowing fast matching of transactions and lookups within the Tree. For instances where the number of events becomes too great to be stored entirely in memory, the least relevant events are stored in a SQLite Database, allowing the program to handle large number of transactions without impacting the performance of the order book too drastically.
This program includes a user interface to display the current market price and order books. 

## Setup/Installation

#### Python version: python 2.7.10

#### Packages Dependencies

###### tkinter, PIL, sqlite3

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
 
 Use the input -i flag to pre-load transactions for the program from a csv file.
 Use the verbose -v flag to show messages from background threads.
 Use the -d display flag to show a display for the order book.
 
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


## Team Members:

Nicholas Yeow [T06902106] - Singapore University of Technology and Design

Tan Kwan Fu [T06501101] - Singapore University of Technology and Design

Angela Yung [T06902101] - University of California, Santa Barbara

Yifan Li [T06901110] - Team China

Deniz Sen [T06303125] - Team Germany

Yao-Cheng Zhang [B04902047] - National Taiwan University
