import sys

import os
import paramiko
import misc_tools
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
#from log import logger
import logging
import getpass
import subprocess
import sys
"""
A lot of this code is adapted from Todd Birchard's Fantastic Paramiko SSH/SCP Tutorial:
https://hackersandslackers.com/automate-ssh-scp-python-paramiko/
https://github.com/hackersandslackers/paramiko-tutorial
"""

class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, gitServer, pxe, user, pxe_user, ssh_key_filepath, git_ssh_key_filepath, known_hosts_filepath, remote_path, gitServer2):
        self.gitServer = gitServer #gitserver ip
        self.pxe = pxe #pxe server ip
        self.user = user #gitserver username
        self.pxe_user = pxe_user #pxe server username
        self.gitServer2 = gitServer2 #second git Server IP for sending files back.
        self.known_hosts_filepath = known_hosts_filepath
        self.ssh_key_filepath = ssh_key_filepath #local windows machine path to the ssh id_rsa
        self.git_ssh_key_filepath = git_ssh_key_filepath
        self.remote_path = remote_path #place to put logs
        self.client = None
        self.scp = None
        self.conn = None
        self.query = None  # for asking if ssh key already exists
        #self.upload_ssh_key()manually doing inline now



    def _get_ssh_key(self):
        """
        Fetch locally stored SSH key.
        """
        try:
            print (self.ssh_key_filepath)
            self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
            logging.info(f'Found SSH key at {self.ssh_key_filepath}')
        except SSHException as error:
            logging.error(error)
        return self.ssh_key

    def upload_ssh_key(self):

        while self.query != "yes":
            self.query = str.lower(input("Did you already send your ssh to the git server? "))
            if self.query == "no" or self.query == "n":
                try:
                    print(self.ssh_key_filepath,self.gitServer)
                    """
                    Original Meant for a UNIX/LINUX system
                    
                    os.system(f'ssh-copy-id -i {self.ssh_key_filepath} {self.user}@{self.gitServer}>/dev/null 2>&1')
                    os.system(f'ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.gitServer}>/dev/null 2>&1')
                   """


                    print("SENDING OUR KEY TO THE GIT SERVER!")
                    cmd = f"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe type {self.ssh_key_filepath}.pub | ssh {self.user}@{self.gitServer} \"cat >> ~/.ssh/authorized_keys\""
                    print(cmd)
                    """Have to disable the line below because it causes Pycharm to hang up"""
                    subprocess.call(cmd, shell=True)



                    """
                    print("KEY SUCCESSFULLY SENT!")
                    cmd = f"scp {self.user}@{self.gitServer}:~/.ssh/id_rsa {self.git_ssh_key_filepath}"
                    try:
                        subprocess.call(cmd)
                        print("Received key from git!")
                    except:
                        print("Couldn't get key from git!")
                    """
                    #logging.info(f'{self.ssh_key_filepath} uploaded to {self.gitServer}')
                except FileNotFoundError as error:
                    logging.error(error)
                    sleep(3)
            elif self.query == "yes" or self.query == "y":
                self.query = "yes"
                print("Skipping the ssh key copy")




    def _connect(self):
        """
        Open connection to remote host.
        """
        if self.conn is None:
            try:
                self.client = paramiko.SSHClient()
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(AutoAddPolicy())
                self.client.connect(
                    self.gitServer,
                    username=self.user,
                    key_filename=self.ssh_key_filepath,
                    look_for_keys=True,
                    timeout=5000
                )
                #chan = self.client.invoke_shell()
                self.scp = SCPClient(self.client.get_transport())
            except AuthenticationException as error:
                logging.error(f'Authentication failed: did you remember to create an SSH key? {error}')
                raise error
        return self.client

    def disconnect(self):
        """Close ssh connection."""
        if self.client:
            self.client.close()
        if self.scp:
            self.scp.close()

    def execute_cmd_git(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """
        self.conn = self._connect()
        output = []
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            print("EXECUTING IN GIT\n"
                  "______________________________")
            print (cmd)
            for line in response:
                #print(f'INPUT: {cmd} | OUTPUT: {line}')
                line = line.replace("\n", "")
                print (line)
                output.append(line)
        return (output)

    def execute_cmd_pxe(self, commands):
        """
        This version is meant to be used with the pxe and not the git server
        Execute multiple commands in succession.


        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """
        self.conn = self._connect2()
        output = []
        print("EXECUTING IN PXE\n"
              "______________________________")
        for cmd in commands:
            stdin, stdout, stderr = self.remote_client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            print (cmd)
            for line in response:
                #print(f'INPUT: {cmd} | OUTPUT: {line}')
                line = line.replace("\n", "")
                print(line)
                output.append(line)
        return (output)

    def _connect2(self): #we need to go deeper
        """
        This is specifically for the second ssh session into the PXE after bouncing off the git server
        Taken from:
        https://stackoverflow.com/questions/18968069/paramiko-port-forwarding-around-a-nat-router/19039769#19039769
        modified to work within this class
        """
        # Set up the proxy (forwarding server) credentials
        proxy_hostname = self.gitServer
        proxy_username = self.user
        proxy_port = 22

        # Instantiate a client and connect to the proxy server
        self.proxy_client = SSHClient()
        self.proxy_client.load_host_keys(self.known_hosts_filepath)
        self.proxy_client.connect(
            proxy_hostname,
            port=proxy_port,
            username=proxy_username,
            key_filename=self.ssh_key_filepath
        )

        # Get the client's transport and open a `direct-tcpip` channel passing
        # the destination hostname:port and the local hostname:port
        transport = self.proxy_client.get_transport()
        dest_addr = (self.pxe, 22)
        local_addr = ('127.0.0.1', 1234)
        channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

        # Create a NEW client and pass this channel to it as the `sock` (along with
        # whatever credentials you need to auth into your REMOTE box
        self.remote_client = SSHClient()
        self.remote_client.load_host_keys(self.known_hosts_filepath)
        self.remote_client.connect(self.pxe,
                                   port=22,
                                   username=self.pxe_user,
                                   key_filename=self.git_ssh_key_filepath,
                                   #password=pxe_password_selection(self.pxe),
                                   sock=channel)

        # `remote_client` should now be able to issue commands to the REMOTE box
        return self.remote_client


    def bulk_upload(self, files):
        """
        Upload multiple files to a remote directory.

        :param files: List of paths to local files.
        :type files: List[str]
        """
        self.conn = self._connect()
        uploads = [self._upload_single_file(file) for file in files]
        logging.info(f'Finished uploading {len(uploads)} files to {self.remote_path} on {self.gitServer}')

    def download_file(self, file):
        """Download file from remote host."""
        if self.conn is None:
            self.conn = self.connect()
        self.scp.get(file)

    def qpn_finder(self, MBSN):
        #originally for qpn. Now used for model and qpn.
        cmd = f"grep -rl {MBSN} /WIN/"
        dirs = self.execute_cmd_pxe([cmd])
        qpn = []
        important_info = {} #this dictionary will be returned with the model name and qpn

        for dir in dirs:
            cmd = f"grep -h \"RACKPN=\" {dir}"
            # print(cmd)
            qpn = self.execute_cmd_pxe([cmd])
            if qpn:
                item = qpn[0]
                item = item.replace("RACKPN=", "")
                item = item.replace("\r", "")
                print(f"{item} WAS FOUND!")
                important_info["QPN"] = item
            cmd = f"grep -ih \"RACKSN=\" {dir}"
            # print(cmd)
            racksn = self.execute_cmd_pxe([cmd])
            if racksn:
                item = racksn[0]
                item = item.replace("RACKSN=", "")
                item = item.replace("\r", "")
                print(f"{racksn} WAS FOUND!")
                important_info["RACKSN"] = item
            cmd = f"grep -ih \"MODEL=\" {dir}"
            # print(cmd)
            model = self.execute_cmd_pxe([cmd])
            if model:
                item = model[0]
                item = item.replace("MODEL=", "")
                item = item.replace("\r", "")
                print(f"{item} WAS FOUND!")
                important_info["MODEL"] = item
                return important_info


