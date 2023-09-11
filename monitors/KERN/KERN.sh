#!/bin/bash -u

##############################################################
#############	    SCRIPT CONFIGURATION        ##############
##############################################################
# Set language to make sure same separator (, and .) config is being used
export LC_ALL=C.UTF-8
# Events to monitor using perf
targetEvents="alarmtimer:alarmtimer_fired,alarmtimer:alarmtimer_start,block:block_bio_backmerge,block:block_bio_remap,block:block_dirty_buffer,block:block_getrq,block:block_touch_buffer,block:block_unplug,cachefiles:cachefiles_create,cachefiles:cachefiles_lookup,cachefiles:cachefiles_mark_active,clk:clk_set_rate,cpu-migrations,cs,dma_fence:dma_fence_init,fib:fib_table_lookup,filemap:mm_filemap_add_to_page_cache,gpio:gpio_value,ipi:ipi_raise,irq:irq_handler_entry,irq:softirq_entry,jbd2:jbd2_handle_start,jbd2:jbd2_start_commit,kmem:kfree,kmem:kmalloc,kmem:kmem_cache_alloc,kmem:kmem_cache_free,kmem:mm_page_alloc,kmem:mm_page_alloc_zone_locked,kmem:mm_page_free,kmem:mm_page_pcpu_drain,mmc:mmc_request_start,net:net_dev_queue,net:net_dev_xmit,net:netif_rx,page-faults,pagemap:mm_lru_insertion,preemptirq:irq_enable,qdisc:qdisc_dequeue,qdisc:qdisc_dequeue,random:get_random_bytes,random:mix_pool_bytes_nolock,random:urandom_read,raw_syscalls:sys_enter,raw_syscalls:sys_exit,rpm:rpm_resume,rpm:rpm_suspend,sched:sched_process_exec,sched:sched_process_free,sched:sched_process_wait,sched:sched_switch,sched:sched_wakeup,signal:signal_deliver,signal:signal_generate,skb:consume_skb,skb:consume_skb,skb:kfree_skb,skb:kfree_skb,skb:skb_copy_datagram_iovec,sock:inet_sock_set_state,task:task_newtask,tcp:tcp_destroy_sock,tcp:tcp_probe,timer:hrtimer_start,timer:timer_start,udp:udp_fail_queue_rcv_skb,workqueue:workqueue_activate_work,writeback:global_dirty_state,writeback:sb_clear_inode_writeback,writeback:wbc_writepage,writeback:writeback_dirty_inode,writeback:writeback_dirty_inode_enqueue,writeback:writeback_dirty_page,writeback:writeback_mark_inode_dirty,writeback:writeback_pages_written,writeback:writeback_single_inode,writeback:writeback_write_inode,writeback:writeback_written"
# Time window per sample
timeWindowSeconds=5
# Number of samples to take (Monitored time will be: timeWindowSeconds*desiredSamples)
#desiredSamples=99999
# Total time monitored (NOT TAKING IN CONSIDERATION TIME BETWEEN SCREENSHOTS)
timeAcumulative=0

##############################################################
#############	      MONITORING LOOP	        ##############
##############################################################
echo "Started monitoring script. . ."

header=$(echo "$targetEvents" | tr ',' '\n' | sed 's/^/"/;s/$/"/' | tr '\n' ',' | sed 's/,$//')

while :
do
	##############################################################
	#############		 DATA COLLECTION	        ##############
	##############################################################
	#	Internet connection check via ping
	if ping -q -c 1 -W 1.5 8.8.8.8 >/dev/null; then
        connectivity="1"
	else
		connectivity="0"
	fi
	timestamp=$(($(date +%s%N)/1000000))
	
	# Perf will monitor the events and also act as a "sleep" between both network captures
    tempOutput=$(perf stat --log-fd 1 -e "$targetEvents" -a sleep "$timeWindowSeconds")

	# Data extraction from perf results
	sample=$(echo "$tempOutput" | cut -c -20 | tr -s " " | tail -n +4 | head -n -2 | tr "\n" "," | sed 's/ //g'| sed 's/.$//')
	seconds=$(echo "$tempOutput" | tr -s " " | cut -d " " -f 2 | tail -n 2 | tr ',' '.')

	# Cumulative sum of seconds calculation
	timeAcumulative=$(awk "BEGIN{ print $timeAcumulative + $seconds }")
		
	##############################################################
	#############	           OUTPUT	            ##############
	##############################################################
	
	# Send to server
    server_path = "$SERVER_PATH"
        
	# Check if the header exists
    if [[ ! -f header_added.txt ]]; then
	    kern_file="/$server_path/kern_data.csv"
	    echo "TimeAcumulative,Timestamp,Seconds,Connectivity,$header" | \
	        ssh "$server_path" 'cat > $kern_file'
        touch header_added.txt
	fi

	kern_file="/$server_path/kern_data.csv"
 
	# Append data in the csv file
    echo "$timeAcumulative,$timestamp,$seconds,$connectivity,$sample" | \
        ssh "$server_path" 'cat >> $kern_file'
done
