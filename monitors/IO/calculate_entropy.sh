#!/bin/bash

# specify which directory to monitor
monitor_dir="/"

cleanup(){
  rm -rf ${ScriptDir}/tmp
  exit 0
}

trap cleanup SIGINT

#Server and port to push data
server="http://192.168.31.185"
port="5003"
directory="/sensor/"
mac=$( cat /sys/class/net/eth0/address | tr : _ )

caculate_entropy(){
entropy=$(${pythoncmd} <<EOF
import math
from collections import Counter
try:
  with open('$tmp_path', 'rb') as f:
    data = f.read()
    counter = Counter(data)
    total_bytes = len(data)
    entropy = 0
    for count in counter.values():
      p_x = count / total_bytes
      entropy += - p_x * math.log2(p_x)
    print(entropy)
except FileNotFoundError:
  pass
EOF
)
}

monitor_write_file(){
  inotifywait -q -m -e modify,create --fromfile ${ScriptDir}/fromfile.txt -r $monitor_dir | while read path action file
  do
    if [[ -f "$path$file" && "$file" != *"log"* && "$file" != *"watchdog"* && "$file" != *".swp"* && "$file" != *".tmp"* && "$file" != *".swx"* ]]; then
      timestamp=$(($(date +%s%N)/1000000))
      file_path="$path$file"
      head -c ${header_byte} "${file_path}" >${tmp_path}       
      caculate_entropy
		
      #finalOutput="[$timestamp] $file_path | $action | entropy: $(echo ${entropy}|awk  '{printf "%.6f\n", $0}')"
      num="$(echo ${entropy} | awk '{printf "%.6f", $0}')"
      final="$timestamp,$file_path,$action,$num"
      #echo $finalOutput
      res=$(curl -sk -X POST -d "$final" -H "Content-Type: application/json" "$server:$port$directory$mac")
    fi
  done
}

ScriptDir=$(cd `dirname $0`; pwd)
mkdir -p ${ScriptDir}/tmp
tmp_path=${ScriptDir}/tmp/entropy.txt
pythoncmd="python3"
header_byte=100 #the amount of bytes to calculate; or select randomly: header_byte=`echo $((RANDOM % 101 + 100))` 
monitor_write_file

