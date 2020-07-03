import datetime
import sys
sys.path.insert(1, r"./sensitive template files/" )
from config import *
import menu
from client import RemoteClient
import re
import socket
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

    remote = RemoteClient(gitServer, pxe, user, pxe_user, ssh_key_filepath, known_hosts_filepath, remote_path, gitServer2)
    #create the log folder in the gitserver
    qpn = input("What is the QPN for the Rack? ")
    remote.execute_cmd_git([f'mkdir {remote_path}{project}'])
    remote.execute_cmd_git([f"mkdir {remote_path}{project}/{MBSN}_{qpn}_logs"])
    #find the most recent PRETEST LOG
    current_time = datetime.datetime.now() #find the current time
    year = current_time.year
    print (current_time.month, current_time.day)
    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    months_r = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }



    tests = ["PRETEST", "RUNIN", "FST"]
    for test in tests: #cycle through the tests to find each one.
        done_flag = False #flag for breaking out of loop
        dirs = []

        while dirs == [] or dirs == None:#select all current month dirs
            dirs = remote.execute_cmd_pxe([f"find /RACKLOG/{project}/{year}/* -name {MBSN}"])
            if dirs == []:
                #if we don't find anything
                print("No results for this year for this SN!")
                MBSN = input("Enter in a different SN: ")
                continue
            my_dates = []
            # sorts by date

            reg = re.compile(f'/RACKLOG/{project}/{year}/...\d\d/{MBSN}')
            #print (reg)
            dirs = [string for string in dirs if re.match(reg, string)]
            dirs.sort(key=lambda date: datetime.datetime.strptime(date, f'/RACKLOG/{project}/{year}/%b%d/{MBSN}'), reverse= True)
            print (dirs)
            pass_dir = []
            for dir in dirs:
                pass_dir = remote.execute_cmd_pxe([f"find {dir}/{test} -iname *pass*"])
                if pass_dir != []:
                    remote.execute_cmd_pxe([f"scp -r {dir}/{test} {user}@{gitServer2}:{remote_path}{project}/{MBSN}_{qpn}_logs/"])
                    #print (f"scp -r {dir}/{test} {user}@{gitServer2}:{remote_path}{MBSN}_logs/\n")
                    break
                else:
                    print("Nothing was found\n")

    print("All Done!")
    #below scp needs modification
    os.system("pscp -r doug@192.168.66.28:/home/doug/logs/S5UK_PY C:\Users\douglas.nguyen\Documents\logs")
    hostname = socket.gethostname()
    ip_address = get_ip()
    print(f"IP Address: {ip_address}")
    username = getpass.getuser()
    remote.execute_cmd_git(f"scp -r {remote_path}{project}/{MBSN}_{qpn}_logs/ {username}@{ip_address}:/~")

            #remote.execute_cmd_pxe([f"scp -r {log} {user}@{gitServer2}:{remote_path}{MBSN}_logs/")
            #print (dir, dir_month, dir_day)



            #scan each dir for the test, if found scp it out. then break with the flag or break
            #if not found repeat with next month





    #exit()

#
#def qpn():