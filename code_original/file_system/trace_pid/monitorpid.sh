#!/bin/bash -u
export LC_ALL=C.UTF-8

# Resource monitoring
resourceMonitor=false
# Time window per sample
timeWindowSeconds=5
# Total time monitored (NOT TAKING IN CONSIDERATION TIME BETWEEN SCREENSHOTS)
timeAcumulative=0

touch pidresult.txt

scp pidresult.txt heqing@192.168.0.104:/home/heqing/

echo "Started monitoring script..."

while :
do
    if ping -q -c 1 -W 1.5 8.8.8.8 >/dev/null; then
            connectivity="1"
    else
	    connectivity="0"
    fi


    timeout 10s perf trace -a -T > output.txt 2>&1
						    
    echo "Sending data to: $url"
							        
    scp output.txt heqing@192.168.0.104:/home/heqing/pidresult.txt

    echo "Data sent to server..."

    sleep "$timeWindowSeconds"

done

echo "Monitoring script finished."

