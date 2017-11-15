import tkinter as tk
from PIL import Image, ImageTk

book=tk.Tk()
# basic frame setting:
book.title("Order Book")
book.geometry("1200x800")
book.configure(background='black')
# -----------entries in the book:----------------------
# icon
icon = Image.open("ether.png")
icon = ImageTk.PhotoImage(icon)
ether=tk.Label(book,image=icon,bg='black')
ether.place(x=40,y=20)
# market price.
title=tk.Label(book,text="ETH/USD:",fg='white',bg='black')
title.config(font=("Arial",40))
title.place(x=160,y=20,width=240,height=80)

#-----------order book: Ask, Bid, Trades---------------
book.mainloop()
