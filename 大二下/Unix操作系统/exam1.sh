#!/bin/sh

if [ $# -eq 1 ]; then
	INPUT='x'
	echo  'input anything'
	while [ TRUE ]; do
		read INPUT
		if [ -n "$INPUT" ]; then
			echo $INPUT >> $1
		else
			break
		fi
	done
	cat $1
else
	echo "Usage: exam1.sh filename"
fi

