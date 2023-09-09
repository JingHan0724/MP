#!/bin/bash -u
export LC_ALL=C.UTF-8

#	Events to monitor using perf
targetEvents="filemap:*,jbd2:*,writeback:*,ext4:*,block:*"
#	Resource monitoring
resourceMonitor=false
#	Time window per sample
timeWindowSeconds=5
#	Number of samples to take (Monitored time will be: timeWindowSeconds*desiredSamples)
#desiredSamples=99999
#	Total time monitored (NOT TAKING IN CONSIDERATION TIME BETWEEN SCREENSHOTS)
timeAcumulative=0


# Server and port to push data
server="http://192.168.0.104"
port="5002"
sensorid="b8_27_eb_29_df_81"  # Replace with the correct sensor ID
url="$server:$port/sensor/$sensorid"
mac=$(cat /sys/class/net/eth0/address | tr : _ )

echo "Started monitoring script..."

while :
do
    if ping -q -c 1 -W 1.5 8.8.8.8 >/dev/null; then
        connectivity="1"
    else
        connectivity="0"
    fi

    timestamp=$(($(date +%s%N)/1000000))

    # Perf will monitor the events and also act as a "sleep" between both network captures
    tempOutput=$(perf stat --log-fd 1 -e "$targetEvents" -a sleep "$timeWindowSeconds")

    # Extracting data from perf results
    sample=$(echo "$tempOutput" | cut -c -20 | tr -s " " | tail -n +4 | head -n -2 | tr "\n" "," | sed 's/ //g'| sed 's/.$//')
    seconds=$(echo "$tempOutput" | tr -s " " | cut -d " " -f 2 | tail -n 1 | tr "," ".")

    # Cumulative sum of seconds calculation
    timeAcumulative=$(awk "BEGIN{ print $timeAcumulative + $seconds }")

    # Constructing the data to send
    finalOutput="$timeAcumulative,$timestamp,$seconds,$connectivity,$sample"

    # Sending data to the server
    echo "Sending data to: $url"
    res=$(curl -sk -X POST -d "$finalOutput" -H "Content-Type: application/json" "$url")

    echo "Data sent to server..."

    sleep "$timeWindowSeconds"
done

echo "Monitoring script finished."

