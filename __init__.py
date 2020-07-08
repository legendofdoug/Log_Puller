
from fai import *
import time
#from .files import fetch_local_files

import menu
import sys
import os
from os import walk
import pysftp
from time import sleep


def main():
    #Initialize the remote client session and execute actions.
    #print (host, user, ssh_key_filepath, remote_path)
    #print (os.path.exists(ssh_key_filepath))
    #print(os.path.exists(remote_path))
    print ("START")
    selection = menu.menu_selection()
    print ("SELECTION DONE")
    print (selection)
    if selection == "1":
        fai()
    elif selection == "q" or selection == "quit":
        exit()
    else:
        print ("Invalid Selection")

    #func_options[selection]



    #dir = input("What is the directory you want? ")

    #r:wemote.execute_cmd(f"ls {dir}")
    #list_files(remote, dir)
    #time.sleep(5)
    #test again







main()

