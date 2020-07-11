
from fai import *
import time
#from .files import fetch_local_files
import getpass
import menu
import sys
import os
from os import walk
import pysftp
from time import sleep


def main():
    selection = menu.menu_selection()
    if selection == "1":
        fai()
    elif selection == "q" or selection == "quit":
        exit()
    else:
        print ("Invalid Selection")
    input("ALL DONE! Enter anything to quit!")









main()

