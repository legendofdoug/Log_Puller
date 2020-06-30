from log_scripts import *
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

    selection = menu.menu_selection()
    func_options = {
        1: fai(),
        2: qpn(),
        3: rackid(),
        4: mbsn(),
        5: specificIssue(),
    }
    if (selection == "q" or selection == "quit" or selection == "exit"):
        exit()
    func_options[selection]



    #dir = input("What is the directory you want? ")

    #r:wemote.execute_cmd(f"ls {dir}")
    #list_files(remote, dir)
    #time.sleep(5)
    #test







main()

