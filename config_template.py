"""Remote host configuration."""
import os

from os import environ, path
from dotenv import load_dotenv

# Load environment variables from .env
#basedir = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(basedir, '.env'))



# Read environment variables
gitServer = ''#git Server IP goes here
user = 'doug' #User name goes here
ssh_key_filepath = "" #path to id_rsa file goes here
known_hosts_filepath = "" #path to known_hosts file goes here
remote_path = '' #path on git server where you weant to save files



local_file_directory = '' #this is the path to the remote directory to target for file transfers.
#it is essentially a place to stage your uploads and downloads.


