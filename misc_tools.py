import socket
import argparse, os
from subprocess import call
from config import *
import os
import getpass



#function below is from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
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

def pxe_user_selection():
    answer = str.lower(input("Is pxe username root? "))
    if answer == "yes" or answer == "y" or answer == "true":
        pxe_user = "root"
    else:
        pxe_user = getpass.getuser("What is the username you want to use? ")
    return pxe_user

def winToPosix(win):
    """Converts the specified windows path as a POSIX path in msysgit.

    Example:
    win: C:\\home\\user
    posix: /c/home/user
    """

    posix = win.replace('\\', '/')
    return "/" + posix.replace(':', '', 1)


def ssh_copy_id():
    """ssh-copy-id for Windows.
    Written by cielfors
    https://gist.github.com/ceilfors/fb6908dc8ac96e8fc983
    Example usage: python ssh-copy-id.py ceilfors@my-remote-machine

    This script is dependent on msysgit by default as it requires scp and ssh.
    For convenience you can also try that comes http://bliker.github.io/cmder/.


    This has been modified to fit our use
    """



    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--identity_file", help="identity file, default to ~\\.ssh\\idrsa.pub", default=os.environ['HOME']+"\\.ssh\\id_rsa.pub")
    parser.add_argument("-d", "--dry", help="run in the dry run mode and display the running commands.", action="store_true")
    parser.add_argument("remote", metavar="user@machine")
    args = parser.parse_args()
    """
    local_key = ssh_key_filepath+".pub"
    remote_key = "/home/doug/.ssh/temp_id_rsa.pub"
    print (local_key)

    # Copy the public key over to the remote temporarily
    pw = getpass.getpass(prompt="Enter in the password  for the git server: ", stream=None)

    scp_command = "pscp -pw {} {} {}@{}:{}".format(pw, local_key, user, gitServer, remote_key)
    call(scp_command)




    # Append the temporary copied public key to authorized_key file and then remove the temporary public key
    ssh_command = ("ssh {}@{} ;"
                     "mkdir ~/.ssh;"
                     "touch ~/.ssh/authorized_keys;"
                     "cat {} >> /home/doug/.ssh/authorized_keys;"
                     "rm {};").format(user, gitServer, remote_key, remote_key)
    print(ssh_command)
    call(ssh_command)

