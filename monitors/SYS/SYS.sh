#!/bin/bash

################################################################
###################          Setup           ###################
################################################################
usage() { echo "Usage: $0 [-d <string>] [-s <int> in seconds] [-t <string>, for example '2 days'] [-s <int>] [-p <string>]" exit 0; }

digit='^[0-9]+$'

while getopts "d:h:i:t:s:c" arg; do
	case $arg in
		d)
			RSYNC_PATH=$OPTARG
			;;
		h)
			usage
			exit
			;;
		i)
			RESULTS_PATH=$OPTARG
			;;
		t)
			TIME=$OPTARG
			;;
		s)
			SLEEP=$OPTARG
			[[ ($SLEEP == "$digit") && ($SLEEP -ge 0) ]] || usage
			;;
		c) 
			ITER_MAX=$OPTARG
			[[ ($SLEEP == "$digit") && ($SLEEP -ge 1) ]] || usage
			;;
		*)
			usage
			;;
	esac
done


if [ -z "$RSYNC_PATH" ]
then
	exit 1
fi

if [ -z "$RESULTS_PATH" ]
then
	exit 1
fi

if [ -z "$TIME" ]
then
	TIME="2 days"
fi

if [ -z "$SLEEP" ]
then
	SLEEP=10
fi

echo "Starting monitoring script"

Unix_time_current=$(date +%s)
Unix_time_start_plus= Unix_time_start_plus=$(date +%s --date="$TIME")
echo "Running the monitor for $TIME"
echo "Timestamp start: " "$Unix_time_current"
echo "Time in $TIME: " "$Unix_time_start_plus"
echo "Results path on the device: " "$RESULTS_PATH"
echo "Rsync path on the device: " "$RSYNC_PATH"
counter=0
################################################################
##############          Monitoring Loop           ##############
################################################################
while [[ "$Unix_time_current" -le "$Unix_time_start_plus" ]]


################################################################
###############          Data Transfer           ###############
################################################################
do
	if [[ "$counter" -ge "$ITER_MAX" ]]
	then
		counter=0
		for filename in "$RESULTS_PATH/"*
		do 
			echo "$filename"
            echo "Transfering data to server ..."
			rsync -z --chmod=ugo=rwX --remove-source-files "$filename" "$RSYNC_PATH" &			 
		done
	fi

################################################################
##########          Data Gathering + Output           ##########
################################################################
	echo "Time now: " "$Unix_time_current"	
	echo "Gathering Syscalls"
	UPTIME=$(cat /proc/uptime | awk '{print $1}')
	EPOCH=$(date +%s.%3N)
	# Needs to be the current timestamp
	Date_Hourly=$(date +%s)
		
	perf trace -S -T -o "$RESULTS_PATH/""${Date_Hourly}".log -e !nanosleep -a -- sleep "$SLEEP"
	echo -e "EPOCH: $EPOCH \nUPTIME:$UPTIME" >> "$RESULTS_PATH/""${Date_Hourly}".log &
	Unix_time_current=$(date +%s)
	counter=$((counter+1))
done
################################################################
###############          Data Transfer           ###############
################################################################
echo "cleanup results directory"
for filename in "$RESULTS_PATH/"*
	do
		echo "$filename"
		rsync -z --chmod=ugo=rwX --remove-source-files "$filename" "$RSYNC_PATH" &
	done
echo "exited MonitoringScript"
exit 0
