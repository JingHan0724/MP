#!/bin/bash

# Default monitor interval (in seconds)
monitor_interval=10

#Server and port to push data
server="http://192.168.31.185"
port="5002"
directory="/sensor/"
mac=$( cat /sys/class/net/eth0/address | tr : _ )

# Main monitoring loop
while true; do
    # Display date and time
    timestamp=$(($(date +%s%N)/1000000))

    # Display I/O statistics using iostat
    iostat_output=$(iostat -d -x 10 2 | grep '[0-9]' | tail -n 1) # the name of the block device
    read_ops=$(echo "$iostat_output" | awk '{print $4}') # number of read I/O operations per second
    write_ops=$(echo "$iostat_output" | awk '{print $5}') # number of write I/O operations per second
    read_kbs=$(echo "$iostat_output" | awk '{print $6}') # kilobytes read per second
    write_kbs=$(echo "$iostat_output" | awk '{print $7}') # kilobytes read per second
    avgrq_sz=$(echo "$iostat_output" | awk '{print $8}') # average size (in sectors) of the requests sent to the device
    avg_queue=$(echo "$iostat_output" | awk '{print $9}') # average queue length (number of requests waiting for service)
    await=$(echo "$iostat_output" | awk '{print $10}') # average time (in milliseconds) for I/O requests to be serviced (including queue time)
    r_await=$(echo "$iostat_output" | awk '{print $11}') #average time (in milliseconds) for read requests to be serviced
    w_await=$(echo "$iostat_output" | awk '{print $12}') #average time (in milliseconds) for written requests to be serviced
    svctm=$(echo "$iostat_output" | awk '{print $13}') #average service time (in milliseconds) for I/O requests
    util=$(echo "$iostat_output" | awk '{print $14}') #percentage of time the device was busy servicing I/O requests.

    # Calculate disk utilization percentage
    # disk_utilization=$(df -h | grep "/dev/$device" | awk '{print $5}' | sed 's/%//')
	
    #PUSH to server	
    finalOutput="$timestamp,$read_ops,$write_ops,$read_kbs,$write_kbs,$avgrq_sz,$avg_queue,$await,$r_await,$w_await,$svctm,$util"
    res=$(curl -sk -X POST -d "$finalOutput" -H "Content-Type: text/csv" "$server:$port$directory$mac")

    # Sleep for a while before the next iteration
    #sleep $monitor_interval
done
