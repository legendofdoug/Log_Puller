import datetime
import sys
from config import *
import menu
from client import RemoteClient
import re
import socket
import getpass
import misc_tools
sys.path.insert(1, r"./sensitive template files/")



def fai():
    print("______________________________________________\n"
          "STARTING FAI LOG COLLECTION\n"
          "______________________________________________\n")
    MBSN = input("Enter the MBSN or whatever the log files use:  ")
    #MBSN = "AWS00400810"
    project = menu.project_selection()
    pxe = menu.pxe_selection()
    #project = "S5U_PY"
    #pxe = "192.168.0.83"
    # pxe_password = menu.pxe_password_selection(pxe)
    # pxe_user = menu.pxe_user_selection() #In case I want to change pxe user later
    pxe_user = "root"
    print(f"You have entered:\n"
          f"MBSN: {MBSN}\n"
          f"Project: {project}\n"
          f"PXE: {pxe}\n")

    remote = RemoteClient(gitServer, pxe, user, pxe_user,
                          ssh_key_filepath, known_hosts_filepath,
                          remote_path, gitServer2)
    remote.upload_ssh_key()
    # create the log folder in the gitserver
    #qpn = input("What is the QPN for the Rack? ")
    qpn = remote.qpn_finder(MBSN, project)
    remote = RemoteClient(gitServer, pxe, user, pxe_user,
                          ssh_key_filepath, known_hosts_filepath,
                          remote_path, gitServer2)
    print (qpn)
    git_project_path = f"{remote_path}{project}_{MBSN}_{qpn}_logs"
    #Below is key exchange
    #putting the git key onto the pxe server
    git_key = remote.execute_cmd_git(["cat ~/.ssh/id_rsa.pub"])
    check = remote.execute_cmd_pxe([f"grep {git_key[0]} ~/.ssh/authorized_keys"])
    if not check:
        remote.execute_cmd_pxe([f"echo {git_key[0]} >> ~/.ssh/authorized_keys"])
    #putting the pxe key onto the git server.
    pxe_key = remote.execute_cmd_pxe(["cat ~/.ssh/id_rsa.pub"])
    check = remote.execute_cmd_git([f"grep {git_key[0]} ~/.ssh/authorized_keys"])
    if not check:
        remote.execute_cmd_git([f"echo {pxe_key[0]} >> ~/.ssh/authorized_keys"])


    # remote.execute_cmd_git([f'mkdir {remote_path}{project}'])
    remote.execute_cmd_git([f"mkdir {git_project_path}"])
    # find the most recent PRETEST LOG
    current_time = datetime.datetime.now()  # find the current time
    year = current_time.year
    print(current_time.month, current_time.day)
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

    """
    This loop will find all folders related to the MBSN/SN of the project selected.
    It will then sort them by most recent and then SCP that entire folder over. (Folder cleanup happens next loop)
    
    
    """

    tests = ["PRETEST", "RUNIN", "FST"]
    for test in tests:  # cycle through the tests to find each one.
        # done_flag = False #flag for breaking out of loop
        dirs = []

        while dirs == [] or dirs == None:
            dirs = remote.execute_cmd_pxe([f"find /RACKLOG/{project}/{year}/* -name {MBSN}"])
            if dirs == []:
                # if we don't find anything
                print("No results for this year for this SN!")
                MBSN = input("Enter in a different SN: ")
                continue
            my_dates = []
            # sorts by date

            reg = re.compile(f'/RACKLOG/{project}/{year}/...\d\d/{MBSN}')
            # print (reg)
            dirs = [string for string in dirs if re.match(reg, string)]
            dirs.sort(key=lambda date: datetime.datetime.strptime(date, f'/RACKLOG/{project}/{year}/%b%d/{MBSN}'),
                      reverse=True)
            print(dirs)
            pass_dir = []
            for dir in dirs:
                pass_dir = remote.execute_cmd_pxe([f"find {dir}/{test} -iname *pass*"])
                if pass_dir != []:
                    remote.execute_cmd_pxe([f"scp -r {dir}/{test} {user}@{gitServer2}:{git_project_path}"])
                    # print (f"scp -r {dir}/{test} {user}@{gitServer2}:{remote_path}{MBSN}_logs/\n")
                    break
                else:
                    print("Nothing was found\n")

        """
        This loop is to clear out the failed logs. 
        It's technically inefficient, but I'm too lazy to change it. 
        And I'd rather copy over too much than too little.
        """

    dirs = remote.execute_cmd_git([f"find {git_project_path} -iname *fail*"])
    for dir in dirs:
        remote.execute_cmd_git([f"rm -rf {dir}"])
    # below scp needs modification

    remote.execute_cmd_git([f"cd {git_project_path}; zip -r {remote_path}{project}_{MBSN}_{qpn}_logs.zip ./"])
    cmd = f"pscp -r -scp  {user}@{gitServer}:{remote_path}{project}_{MBSN}_{qpn}_logs.zip C:\\Users\\douglas.nguyen\\Documents\\logs"
    print (cmd)
    os.system(cmd)

    # remote.execute_cmd_git(f"scp -r {remote_path}{project}/{MBSN}_{qpn}_logs/ {username}@{ip_address}:/~")

    # remote.execute_cmd_pxe([f"scp -r {log} {user}@{gitServer2}:{remote_path}{MBSN}_logs/")
    # print (dir, dir_month, dir_day)

    # scan each dir for the test, if found scp it out. then break with the flag or break
    # if not found repeat with next month
    print("All Done!")
