#!/bin/bash

record_time=$1
output_file=$2

echo "Record ..."
perf record -e filemap:* -e jbd2:* -e writeback:* -e block:* -e ext4:* -e cifs:* -a -- sleep $record_time

echo "Data processing ..."
perf report -i perf.data > report_output.txt
cat report_output.txt | grep Samples | grep event > $output_file

#delete intermediate files
rm report_output.txt
rm perf.data*
