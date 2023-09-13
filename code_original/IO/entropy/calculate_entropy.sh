#!/bin/bash

monitor_interval=10 # Set the monitor interval in seconds

cleanup(){
    rm -f lsof_info.txt
    exit 0
}

trap cleanup SIGINT

#Server and port to push data
server="http://192.168.31.185"
port="5002"
directory="/sensor/"
mac=$( cat /sys/class/net/eth0/address | tr : _ )

caculate_entropy(){
entropy=$(${pythoncmd} <<EOF
import math
from collections import Counter
with open('$file_path', 'rb') as f:
    data = f.read()
counter = Counter(data)
total_bytes = len(data)
entropy = 0
for count in counter.values():
  p_x = count / total_bytes
  entropy += - p_x * math.log2(p_x)
print(entropy)
EOF
)
}

monitor_write_file(){
  while true; do
    title="========== Monitoring Round: $(date '+%F +%T') =========="
    res=$(curl -sk -X POST -d "$title" -H "Content-Type: application/json" "$server:$port$directory$mac")	
    lsof >${lsof_file}
    cat ${lsof_file}| tr -s ' ' ','|grep ',REG,'|grep ',[0-9]\+[uw],'|awk -F',' '{print $NF}'|sort -u|while read -r Line;do
      #echo "========Caculate Entropy File[ ${Line} ]"
      file_path="${Line}"
      caculate_entropy
      #PUSH to server	
      finalOutput="entropy: $(echo ${entropy}|awk  '{printf "%.6f\n", $0}') | filePath: [ ${file_path} ]"
      res=$(curl -sk -X POST -d "$finalOutput" -H "Content-Type: application/json" "$server:$port$directory$mac")
    done
    rm -rf ${lsof_file}    
    sleep "${monitor_interval}"
  done
}

ScriptDir=$(cd `dirname $0`; pwd)
pythoncmd="python3"
lsof_file="${ScriptDir}/lsof_info.txt"
monitor_write_file
