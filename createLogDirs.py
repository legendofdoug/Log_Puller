#!/usr/bin/python
import os
import sys

arr = ["PRETEST","RUNIN","FST"]
if len(sys.argv) != 1:
	if sys.argv[1] == "-d":#delete function
		for i in arr:
			print("Deleting "+i)
			os.system("rm -d ./"+i)
	if sys.argv[1] == "-h":#Help function
		
		print("Function to create 3 folders, PRETEST, RUNIN, FST")
		print("Usage: createLogsDirs [arg] [Rack SN]")
		print("-d: Delete the 3 directories")
			
	else:	#creates the folder for the specified rack ID and puts the folders in there
		print (sys.argv[1])
		print "Creating Subdirectories for"+sys.argv[1]
		cmd = "mkdir "+sys.argv[1]
		os.system(cmd)
		for i in arr:
			os.system("mkdir ./"+sys.argv[1]+"/"+i)

else: 	
	print "Creating Subdirectories HERE!"
	for i in arr:
		os.system("mkdir ./"+i)
print "All Done!"
