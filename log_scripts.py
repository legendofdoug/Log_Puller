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

    remote = RemoteClient(gitServer, pxe, user, pxe_user, ssh_key_filepath, known_hosts_filepath, remote_path, gitServer2)
    #create the log folder in the gitserver
    #remote.execute_cmd_git([f"mkdir {remote_path}{MBSN}_logs"])
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
    """
    dirs = []
    while dirs == [] or dirs == None:
        dirs = remote.execute_cmd_pxe([f"find /RACKLOG/{project}/{year}/ -name {MBSN}"])
        if dirs  == [] or dirs == None:
            print ("NO Results found! Try another SN!")
            MBSN = input("Enter the MBSN or whatever the log files use:  ")
    """


    tests = ["PRETEST", "RUNIN", "FST"]
    for test in tests: #cycle through the tests to find each one.
        done_flag = False #flag for breaking out of loop
        #cycle through current month first. starting with the current date then working backwards.
        current_month = current_time.month
        while done_flag == False:
            dirs = []

            while dirs == [] or dirs == None:#select all current month dirs
                dirs = remote.execute_cmd_pxe([f"find /RACKLOG/{project}/{year}/{months_r[current_month]}* -name {MBSN}"])
                if dirs == [] or dirs == None:
                    print("NO Results found for this month! Trying last month")
                    current_month = current_month - 1
                if current_month == 0:
                    print("No results for this year for this SN!")
                    break
                #print (dirs)
                dir_days = []
                for dir in dirs:  # this will cycle through all the available directories
                    #check if the logs have the current test.
                    test_check = remote.execute_cmd_pxe([f"find {log} -iname {test}"])
                    if pass_check == []:
                        pass
                    dir_date = dir.replace(f"/RACKLOG/{project}/{year}/", "")
                    dir_date = dir_date.replace(f"/{MBSN}", "")
                    dir_month = dir_date[0:3]
                    dir_day = dir_date[3:]
                    dir_days.append(int(dir_day)) #this will allow me to sort the days that have passed
                dir_days = dir_days.sort(reverse= True)
                remote.execute_cmd_pxe([f"scp -r {log} {user}@{gitServer2}:{remote_path}{MBSN}_logs/")
                #print (dir, dir_month, dir_day)

                test_logs = remote.execute_cmd_pxe([f"find {dir} -iname {test}"])
                if test_logs == None or test_logs == []:
                    pass
                else:
                    for log in test_logs:
                        folder_dir = remote.execute_cmd_pxe([f"find {log} -iname *pass*"])  # only pick pass folders
                        if folder_dir != [] or folder_dir != None:
                            remote.execute_cmd_pxe([f"scp -r {log} {user}@{gitServer2}:{remote_path}{MBSN}_logs/")
                            break
                print (test_logs)
                done_flag = True
                break



            #scan each dir for the test, if found scp it out. then break with the flag or break
            #if not found repeat with next month





"""
            if months[dir_month] == current_time.month:
                if dir_day == current_time.day + 1: #the +1 is for decrepancies in dates.
                    test_logs = remote.execute_cmd_pxe([f"find {dir} -iname {test}"]) #check for test folder
                    if test_log == None or test_log == "":
                        pass
                    else:
                        folder_dir = []
                        for log in test_logs:
                            folder_dir = remote.execute_cmd_pxe([f"find {log} -iname *pass*"]) #only pick pass folders
                            if folder_dir != [] or folder_dir != None:
                                remote.execute_cmd_pxe([f"scp -r {log} {user}@{gitServer2}:{remote_path}{MBSN}_logs/")
                                break
"""
    #exit()

#
#def qpn():