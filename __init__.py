#!/usr/bin/python


import gui
import tkinter as tk

def main():
    while True:
        root = tk.Tk()
        gui.log_gui(root)
        root.mainloop()

    """selection = menu.menu_selection()
    if selection == "1":
        fai()
    elif selection == "q" or selection == "quit":
        exit()
    else:
        print ("Invalid Selection")

    input("ALL DONE! Enter anything to quit!")"""

main()

