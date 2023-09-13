#!/bin/bash

# Loop through all subdirectories in the root directory, excluding /dev
for MONITOR_DIR in $(ls -d /*/ | grep -vE '^/dev/|^/proc/'); do
    # Start a background process to monitor using inotifywait
    inotifywait -m -r --timefmt '%d/%m/%Y %H:%M' --format '%T %w %f %e' -e move,create,delete,modify $MONITOR_DIR | while read date time dir file event
    do
      # Redirect the output to output.txt and suppress terminal output
      echo "[$date $time] File: $dir$file Event: $event" > output.txt
    done &
done

# Wait for all background processes
wait