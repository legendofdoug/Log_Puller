import socket
import argparse, os
from subprocess import call
from config import *
import os
import getpass
"""This file is no llonger used, but is being kept just in case I need it."""

# function below is from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def pxe_user_selection(): #will only be used if we see a pxe that doesn't use root
    answer = str.lower(input("Is pxe username root? "))
    if answer == "yes" or answer == "y" or answer == "true":
        pxe_user = "root"
    else:
        pxe_user = getpass.getuser("What is the username you want to use? ")
    return pxe_user





