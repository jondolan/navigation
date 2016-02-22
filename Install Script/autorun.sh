#!/bin/bash

# Usage of /media/IEEE/autorun.sh
#
# Options:
# 	force		(optional)		force copy/install of packages
# 			  			 		default behavior is to copy and install ONLY if directory IEEEInstallFiles does not exist
#
#	run		(optional)		autorun the server code (autorun.py)

FORCE=$( echo $@ | grep -ic 'force' )
RUN=$( echo $@ | grep -ic 'run' )


ADIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IDIR=~/IEEEInstallFiles
CDIR=~/IEEECode

echo 'Copying code...'
rm -rf $CDIR > /dev/null 2>&1 # copy code regardless
mkdir $CDIR
chmod -R 775 $CDIR
cp $ADIR/code/* $CDIR

if [ -d "$IDIR" ]; then # if directory exists
	echo 'Directory exists...'
	if [ $FORCE -gt 0 ]; then # if force is passed, then delete it
		echo 'Deleting directory...'
  		rm -rf $IDIR
	else
		if [ $RUN -gt 0 ]; then # if run is passed
			echo 'Autorunning...'
			cd $CDIR
			python client.py
			exit
		fi
	fi
fi
echo 'Making directory...'
mkdir $IDIR
chmod -R 775 $IDIR
cp $ADIR/packages/* $IDIR
cd $IDIR
python install.py
if [ $RUN -gt 0 ]; then # if run is passed
	echo 'Autorunning...'
	cd $CDIR
	python client.py
fi
