<h1>Log Puller</h1>
<h2>Author: Douglas Nguyen</h2>

<h3>In a nutshell:</h3>
Log Pulling system. Specificially for pulling logs from a server behind a proxy server.

<h3>Vision:</h3>
This program is envisioned to have as minimal User interaction in the log pulling process as possible (which has become a repeated pain at work)
The goal is to have a double click to start, a mode selection, a pxe server, and a Serial Number. That serial number will look for the configuration and pull projects information, part numbers and anything necessary. It also handles ssh/scp keys between the servers. 

The main challenge is the architecture (PC -> GIT -> PXE) and the fact that our system is windows. The PC cannot directly access the PXE because it lives in a different VLAN. So we use the GIT server as a "bounce" and to stage files.

<h3><u>Prerequisites</h3></u>
- Make sure you have ssh keys. This can be done with ssh-keygen
- Have Python 3 and Python Package Paramiko


<h3><u>Setup</h3></u>
1.  When running for first time you must manually generate your own config.py and menu.py (If you work for quanta, you can just grab our Quanta menu from me)
2.  Start __init__.py
3.  The menu will show the functions. Select one..
4. Follow onscreen instructions.
