#!/bin/bash

touch inotify_result.txt

scp inotify_result.txt heqing@192.168.0.104:/home/heqing/

while true; do
    # Start monitoring and write the output to output.txt
    ./monitor_inotify.sh &
    monitor_pid=$!

    # Wait for 10 seconds
    sleep 10

    # Terminate the monitoring process
    kill -9 $monitor_pid

    # Use scp to copy output.txt to the remote computer
    scp output.txt heqing@192.168.0.104:/home/heqing/inotify_result.txt

    # Wait for 5 seconds
    sleep 5
done