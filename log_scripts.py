import datetime
import sys
sys.path.insert(1, r"./sensitive template files/" )
from config import *
import menu
from client import RemoteClient

def fai():
    print ("______________________________________________\n"
            "STARTING FAI LOG COLLECTION\n"
           "______________________________________________\n")
    MBSN = input("Enter the MBSN or whatever the log files use:  ")
    project = menu.project_selection()
    pxe = menu.pxe_selection()
    #pxe_password = menu.pxe_password_selection(pxe)
    pxe_user = menu.pxe_user_selection()
    print(f"You have entered:\n"
           f"MBSN: {MBSN}\n"
           f"Project: {project}\n"
           f"PXE: {pxe}\n")

    remote = RemoteClient(gitServer, pxe, user, pxe_user, ssh_key_filepath, known_hosts_filepath, remote_path)
    #create the log folder in the gitserver
    remote.execute_cmd_git([f"mkdir {remote_path}{MBSN}_logs"])
    #find the most recent PRETEST LOG
    current_time = datetime.datetime.now() #find the current time
    year = current_time.year
    dirs = remote.execute_cmd_pxe([f"find /RACKLOG/{project}/{year}/ -name {MBSN}"]
    for dir in dirs:
        dir = dir.replace(f"/RACKLOG/{project}/{year}/", "")
        dir = dir.replace(f"/{MBSN}", "")
        print (dir)

    #print (remote.execute_cmd2(["ifconfig"]))


    #rint (output)
    exit()

#
#def qpn():