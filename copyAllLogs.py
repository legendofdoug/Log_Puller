#this script copies all the logs related to the SN, regardless if it passes or not. The arguments given are the SN


import sys
import os
import subprocess
import time
#taken from globalstuff
def ExecuteCmd(command, silent = True, testitem = ""):
        p = subprocess.Popen(command.split(), shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        stdout, stderr = p.communicate()
#        if not silent:
#                logging.info(stdout)
#        if p.returncode != 0:
#                if stderr:
#                        logging.error(stderr)
#                        print 'Stderr output'
#                else:
#                        logging.error(stdout)
#                        print 'Stdout output'
#
#                if testitem != "":
#                        racklog("{0} Fail".format(testitem))
#                #raise NameError(('$s failed:' % command))
#                print "{0} failed".format(command)
        return stdout.split('\n')


SNs = sys.argv[1:]
print (SNs)
for SN in SNs:
	cmd = "find /RACKLOG/S5HF_PY/2020 -iname "+SN
	print (cmd)
	arr = ExecuteCmd(cmd)#searches for the paths
	print (arr)

	for i in arr:
		#i is the path to the log directory
		cmd = "scp -r "+i+" doug@192.168.0.2:/home/doug/logs/QCFDRB2019017/"
		print (cmd)	
		os.system(cmd)
		


