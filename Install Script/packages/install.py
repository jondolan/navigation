import os
import subprocess


packagePath = os.path.dirname(os.path.realpath(__file__)) # current directory
print packagePath
codePath =  packagePath[0:len(packagePath)-12] + "Code"

installFiles = sorted([f for f in os.listdir(packagePath) if f != __file__]) # list all files that are not the install file
print "Installing in this order:\n", installFiles

codeFiles = sorted([f for f in os.listdir(codePath) if f != __file__])

for f in installFiles: # extract and install each package
	os.chdir(packagePath)
	command = "tar -xzf " + f
	f = f[3:len(f)-7]
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	process.wait()
	os.chdir(packagePath + "/" + f)
	output = process.communicate()[0]
	os.system("python setup.py install")

print "\n\n***Done extracting and installing packages***\n\n"

print "Code is stored in " + codePath