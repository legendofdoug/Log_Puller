import sys
from config import *
import menu
from client import RemoteClient
# import getpass
import misc_tools
from subprocess import call
import re


def all_logs(parameter):
    print("______________________________________________\n"
          "STARTING ALL LOG COLLECTION\n"
          "______________________________________________\n")
    racksn = input("Enter the RACK SN: ")
    pxe = menu.pxe_selection()  # must be filled in by user in the menu.py
    pxe_user = "root"
    # pxe_user = menu.pxe_user_selection() #Uncomment this if you want to query user for pxe  user

    remote = RemoteClient(gitServer, pxe, user, pxe_user,
                          ssh_key_filepath, git_ssh_key_filepath,
                          known_hosts_filepath, remote_path, gitServer2)
    # remote.upload_ssh_key() #currently not working properly

    # qpn = input("What is the QPN for the Rack? ")
    print("FINDING INFORMATION ABOUT THIS SN!\n")
    important_info = remote.qpn_finder(racksn)
    # You have to call this Remoteclient again, because the previous method messes with it. Find out more later
    remote = RemoteClient(gitServer, pxe, user, pxe_user,
                          ssh_key_filepath, git_ssh_key_filepath,
                          known_hosts_filepath, remote_path, gitServer2)
    qpn = important_info["RACKPN"]
    model = important_info["MODEL"]
    MBSN = important_info["MLBSN"]
    pdnum = important_info["PDNUM"]
    git_model_path = f"{remote_path}{model}_{racksn}_{MBSN}_{qpn}_logs"
    remote.execute_cmd_git([f"mkdir {git_model_path}"])

    dirs = remote.execute_cmd_pxe([f"grep -rl {pdnum} /RACKLOG/{model}/{year}/*"])
    for dir in dirs:
        dir = dir.replace(f"/RACKLOG/{model}/{year}/", "")
        chassissn = dir[6:20]
        print(f"Using {chassissn}")
        break
    print(f"You have entered:\n"
          f"RACKSN: {racksn}\n"
          f"MLBSN: {MBSN}\n"
          f"MODEL: {model}\n"
          f"QPN: {qpn}\n"
          f"PDNUM: {pdnum}\n"
          f"PXE: {pxe}\n"
          f"CHASSIS SN: {chassissn}\n"
          f"zip: {zip_this}\n"
          )

    tests = ["PRETEST", "RUNIN", "NETTEST", "FST"]
    for test in tests:  # cycle through the tests to find each one.
        # done_flag = False #flag for breaking out of loop
        dirs = []
        SNS = [MBSN, pdnum, chassissn]
        while not dirs:  # so long as the directory array is empty
            for sn in SNS:
                dirs = remote.execute_cmd_pxe([f"find /RACKLOG/{model}/{year}/* -name {sn}"])
                print(sn)
                print(dirs)
                if dirs:  # if something is found
                    break
            print("Broke out of loop")
            print(dirs)

            reg = re.compile(f'/RACKLOG/{model}/{year}/...\d\d/{sn}')
            dirs = [string for string in dirs if re.match(reg, string)]
            dirs.sort(key=lambda date: datetime.datetime.strptime(date, f'/RACKLOG/{model}/{year}/%b%d/{sn}'),
                      reverse=True)
            print(dirs)
            for dir in dirs:
                pass_dir = remote.execute_cmd_pxe([f"find {dir}/{test} -iname *pass*"])
                if pass_dir:
                    remote.execute_cmd_git([f"scp -r {pxe_user}@{pxe}:{dir}/{test} {git_model_path}"])
                    # print (f"scp -r {dir}/{test} {user}@{gitServer2}:{remote_path}{MBSN}_logs/\n")
                    break
                else:
                    print("Nothing was found\n")

        """
        This loop is to clear out the failed logs. 
        It's technically inefficient, but I'm too lazy to change it. 
        And I'd rather copy over too much than too little.
        """

    dirs = remote.execute_cmd_git([f"find {git_model_path} -iname *fail*"])
    for dir in dirs:
        remote.execute_cmd_git([f"rm -rf {dir}"])

    zip = str.lower(input("Do you want to zip?"))
    if zip == "y" or zip == "yes":
        remote.execute_cmd_git([f"cd {git_model_path}; zip -r {remote_path}{model}_{racksn}_{MBSN}_{qpn}_logs.zip ./"])
        cmd = f"scp -r  {user}@{gitServer}:{remote_path}{model}_{racksn}_{MBSN}_{qpn}_logs.zip {local_file_directory}"
    else:
        cmd = f"scp -r  {user}@{gitServer}:{remote_path}{model}_{racksn}_{MBSN}_{qpn}_logs {local_file_directory}"
    print(cmd)
    call(cmd)

def questions():
    passorfail = str.lower(input("Do you need passed logs, failed logs or both?"))
    if passorfail not in ["pass", "fail", "failed", "both", "all"]