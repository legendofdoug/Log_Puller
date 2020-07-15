#!/usr/bin/python
import tkinter as tk

class log_gui(tk.Frame):
    def __init__(self, master = None):

root = Tk()
root.title("Log Puller")
rackSNLabel = Label(root, text="RACK  SN")
rackSNLabel.grid(row=0, column=0, columnspan=1, padx=0, pady=0)
rackSN = Entry(root, width=50, borderwidth=2)
rackSN.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
pxeLabel = Label(root, text="PXE IP")
pxeLabel.grid(row=2, column=0, columnspan=1, padx=10, pady=0)
pxe = Entry(root,width=50, borderwidth=2)
pxe.grid(row=3, column=0, columnspan=3, padx=10, pady=10)


root.mainloop()