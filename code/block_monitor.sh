#!/bin/bash

# Before runing this script, you should install sysstat and bc, the commands are as following:
# sudo apt-get install sysstat
# sudo apt-get install bc
# Function to print horizontal line
print_separator() {
    echo "--------------------------------------------------"
}

# Check if the CSV file exists; if not, create it with headers
if [[ ! -e "block_storage_metrics.csv" ]]; then
    echo "Date and Time,Device,Read Ops/s,Write Ops/s,Avg Queue Length,Disk Utilization (%),IO Service Time ms,I/O Pattern" > block_storage_metrics.csv
fi

# Main monitoring loop
while true; do
    # Display date and time
    current_datetime=$(date +"%Y-%m-%d %H:%M:%S")

    # Display I/O statistics using iostat
    iostat_output=$(iostat -d -x 1 2 | tail -n 1)
    device=$(echo "$iostat_output" | awk '{print $1}')
    read_ops=$(echo "$iostat_output" | awk '{print $4}')
    write_ops=$(echo "$iostat_output" | awk '{print $5}')
    avg_queue=$(echo "$iostat_output" | awk '{print $9}')
    io_service_time=$(echo "$iostat_output" | awk '{print $12}')

    # Calculate disk utilization percentage
    disk_utilization=$(df -h | grep "/dev/$device" | awk '{print $5}' | sed 's/%//')

    # Detect I/O pattern (Rising, Falling, Stable)
    io_pattern="Stable"
    if [[ $read_ops -gt 0 && $write_ops -gt 0 ]]; then
        io_pattern="Mixed"
    elif [[ $read_ops -gt 0 ]]; then
        io_pattern="Read-Heavy"
    elif [[ $write_ops -gt 0 ]]; then
        io_pattern="Write-Heavy"
    fi

    # Append the data to the CSV file
    echo "$current_datetime,$device,$read_ops,$write_ops,$avg_queue,$disk_utilization,$io_service_time,$io_pattern" >> block_storage_metrics.csv

    # Sleep for a while before the next iteration
    sleep 5
done
