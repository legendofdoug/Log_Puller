import sys
import os
import subprocess


SNs = sys.argv[1:]
print (SNs)
for SN in SNs:
	arr = subprocess.check_output("find /RACKLOGS/S5U_PY/ -iname "+SN, shell=True)#searches for the paths
	testArr = test.split("\n")
	for i in testArr:
		#i is the path to the log directory
		cmd = "scp -r "+i+" doug@192.168.0.2:/home/doug/logs/QCFUBR2008004/"+SN
		print (cmd)	
		#os.system(cmd)



