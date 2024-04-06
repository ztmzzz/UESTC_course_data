#!/bin/bash
name=$1
for shuliang in 1000 10000 100000 1000000 10000000 100000000 1000000000
do
	for np in 1 2 4 8 16
	do
		for mode in 1 2 3 11 21 31 32 33 4 5 6
		do
			int=1
			res=0
			while(( $int<=30 ))
			do
				a=$(mpirun -np $np ./$name $shuliang $mode)
				res=`echo "$res + $a" | bc`
				let "int++"
			done
			echo "shuliang=$shuliang;np=$np;mode=$mode;res=$res" >> theout.txt
		done
	done
done