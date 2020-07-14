#!/usr/bin/python

from tkinter import *

root = Tk()
root.title("Log Puller")
rackSNLabel = Label(root, text="RACKSN")
rackSNLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0)
rackSN = Entry(root, width=50, borderwidth=2)
rackSN.grid(row=1, column=0, columnspan=3, padx=10, pady=10)


root.mainloop()