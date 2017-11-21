import Tkinter as tk # capital letter for 2.7 lower letter for 3.5+
from PIL import Image, ImageTk
import numpy as np
import time

def display(askTree, bidTree, trades):
	'''
	run the display
	Input:
		bidtree, asktree, trades
	Output:
	Display: 
		UI 
	'''
	#UI Framework
	UI = tk.Tk()
	APP(UI)
	#APP(UI).UPDATE(askTree,bidTree,trades)
	APP(UI).testUpdate(askTree, bidTree, trades) #this is for test only.
	UI.mainloop()


def FullBook():
	'''
	when the user ask for a full order book, display the static order book of
	that exact moment.
	'''

class APP(tk.Frame):
	def __init__(self,parent):
		'''
		The main UI frame to display:
			contains: current market price of Ethereum
					  bid order book
					  ask order book
					  successful trades
					  full order book button
		'''
		#--------------------Main Display----------------------
		self.book=parent
		# basic frame setting:
		self.book.title("Order Book")
		self.book.geometry("1200x800")
		self.book.configure(background='black')
		# -----------entries in the book:--------
		# icon
		global icon
		icon = Image.open("ether.png")
		icon = ImageTk.PhotoImage(icon)
		ether=tk.Label(self.book,image=icon,bg='black')
		ether.place(x=120,y=20)

		#----market prices---
		# market price.
		title=tk.Label(self.book,text="ETH/USD:",fg='white',bg='black')
		title.config(font=("Arial",40))
		title.place(x=240,y=20,width=240,height=80)
		#high price of today
		high=tk.Label(self.book,text="HIGH",fg='gray',bg='black')
		high.config(font=("Helvetica",20))
		high.place(x=720,y=20,width=120,height=30)
		# low price of today
		low=tk.Label(self.book,text="LOW",fg='gray',bg='black')
		low.config(font=("Helvetica",20))
		low.place(x=720,y=60,width=120,height=30)

		#----Order Books-----
		# three Book names
		self.__book_name(["Bid Book","Ask Book","Trade Book"],100)
		# Book contennt names
		self.__content_name(["COUNT","AMOUNT","TOTAL","PRICE"],0)
		self.__content_name(["PRICE","TOTAL","AMOUNT","COUNT"],400)
		self.__content_name(["TIME","PRICE","AMOUNT"],800)

		#---------------useful buttons----------






	def UPDATE(self,asks,bids,trades):
		"""
		get order tree and transaction records reference, then call the display function
		every to get the display data, convert them into numpy array, save it in the class,
		and finally update the corresponding item in the display.
		update items: two order books: every 1 sec
					  records: every 2 sec
					  current market price: every 10 sec
					  max and min porice of the day: every 10 sec
		Input:
			asks, bids, trades: refenence to the correspoinding functions
		Output:
		"""
		self.bids=bids
		self.asks=asks
		self.trades=trades
		# update records
		self.__updateBook()
		self.__updateRecords()
		# update prices
		return 0

	def testUpdate(self,asks,bids,trades): # this is for test only!
		'''
		use generate test date to test the update functionality of the class.
		Input:
			asks, bids, trades: refenence
		'''
		self.test_times=0 # this is for testing, only iterate for 30 times 
		self.bids=bids
		self.asks=asks
		self.trades=trades
		self.__testUpdate()# update itself every 1 second
		self.__showMarketPrice()
		self.__showMaxMin()
		return 0

	#---------------------private functions------------------------------

	def __book_name(self,names,start):
		"""
		Show different order book names
		Input:
			names: order names
			start: x_axis position to start
		"""
		idx=0
		for name in names:
			book = tk.Label(self.book,text=name,fg='white',bg='black')
			book.config(font=("Helvetica",24))
			book.place(x=start+idx*400,y=200,width=160,height=40)
			idx+=1

	def __content_name(self,names,start):
		'''
		Display the names of the contents in different order books
		Input:
			names: content names
			start: x_axis position to start (in pixels)
		'''
		idx=0
		for name in names:
			content=tk.Label(self.book,text=name,fg='gray',bg='black')
			content.config(font=("Helvetica",18))
			content.place(x=start+idx*100,y=250,width=100,height=40)
			idx+=1

	def __content_row(self,contents,x_start,y_start):
		"""
		show contents of a single row from the order book display matrix
		Normally contains: price, total, amout, count
		Input:
			contents
			x_start: x axis position to start (in pixels)
			y_start: y axis position to start (in pixels)
		"""
		idx=0
		for content in contents:
			num=tk.Label(self.book,text=str(content),fg='gray',bg='black')
			num.config(font=("Helvetica",16))
			num.place(x=x_start+idx*100,y=y_start,width=100,height=40)
			idx+=1

	def __showBook(self,bids,asks):
		"""
		Update Bid Book and Ask book.
		"""
		row=300
		ask=400
		bid=0
		for bid_row in bids:
			self.__content_row(bid_row,bid,row)
			row+=40
		row=300
		for ask_row in asks:
			self.__content_row(ask_row,ask,row)
			row+=40

	def __showTrades(self,trades):
		"""
		Update the trades Book.
		"""
		row=300
		for trade_row in trades:
			self.__content_row(trade_row,800,row)
			row+=40

	def __getPrices(self):
		"""
		get all the successful transaction prices from the DB,
		then compute the current market price and max, min prices
		of a day.
		all in 4 digits
		"""


	def __showMarketPrice(self):
		"""
		show the current market price.
		"""
		title=tk.Label(self.book,text="6900.2366",fg='white',bg='black')
		title.config(font=("Arial",40))
		title.place(x=480,y=20,width=240,height=80)

	def __showMaxMin(self):
		"""
		show the max and min price of the day.
		"""
		high=tk.Label(self.book,text="6933.5326",fg='gray',bg='black')
		high.config(font=("Helvetica",20))
		high.place(x=840,y=20,width=120,height=30)

		low=tk.Label(self.book,text="6898.7833",fg='gray',bg='black')
		low.config(font=("Helvetica",20))
		low.place(x=840,y=60,width=120,height=30)


	def __updateBook(self):
		'''
		update the content during an 1 second interval.
		'''
		self.__showBook(self.bids.fastDisplay(),self.asks.fastDisplay())
		self.book.after(1000,self.__updateBook)

	def __updateRecords(self):
		'''
		update the successful records every 2 seconds
		'''
		self.__showTrades(self.trades.fastDisplay())
		self.book.after(2000,self.__updateRecords)

	def __updatePrices(self):
		"""
		update the market pricews every 10 seconds
		"""
		# compute market prices
		self.__getPrices()
		# update it
		self.__showMarketPrice()
		self.__showMaxMin()
		self.book.after(10000,self.__updatePrices)

	def __testUpdate(self): # this is for test only!
		'''
		iterating funnction to update itself.
		'''
		if self.test_times==29:
			return 0
		# update bids and asks order book
		self.__showBook(self.bids[self.test_times],self.asks[self.test_times]) 
		self.__showTrades(self.trades[self.test_times])
		# update test times
		self.test_times+=1
		# call this function again in one second
		self.book.after(1000,self.__testUpdate)

#---------------------testing functions------------------------

def test(file_name,col=None): # this is for test only!
	'''
	this is for testing the display functionality
	Input: 
		filename: file to read in.
		col: due to the data format reason, need to delete 1 colomns
			for bid, is 1 and for ask, is 3
	Output:
		datas: every 10 prices a group. each group of matrix form 10*4
		use list to store all the groups
	'''
	import pandas as pd
	data=pd.read_csv(file_name,delimiter="\t",header=None)
	if (col):
		del data[col]
	datas=[]
	for row in range(30):
	    start=row*10
	    end=start+9
	    num=data.iloc[start:end,:]
	    num=num.as_matrix()
	    datas.append(num)
	return datas


def UnitTest(): # this is for test only!
	"""
	This is for unit testing.
	I ramdomly choose 30 period of times and store them in csv files. so the maximum 
	update times is 30
	"""
	bids=test("tests/bid_order.csv",1)
	asks=test("tests/ask_order.csv",3)
	trades=test("tests/trades.csv")
	display(asks,bids,trades)

UnitTest() # this is used for test only















