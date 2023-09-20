#!/bin/bash -u
export LC_ALL=C.UTF-8

#	Events to monitor using perf
targetEvents="block:block_bio_backmerge,block:block_bio_bounce,block:block_bio_complete,block:block_bio_frontmerge,block:block_bio_queue,block:block_bio_remap,block:block_dirty_buffer,block:block_getrq,block:block_plug,block:block_rq_complete,block:block_rq_insert,block:block_rq_issue,block:block_rq_remap,block:block_rq_requeue,block:block_sleeprq,block:block_split,block:block_touch_buffer,block:block_unplug,ext4:ext4_alloc_da_blocks,ext4:ext4_allocate_blocks,ext4:ext4_allocate_inode,ext4:ext4_begin_ordered_truncate,ext4:ext4_collapse_range,ext4:ext4_da_release_space,ext4:ext4_da_reserve_space,ext4:ext4_da_update_reserve_space,ext4:ext4_da_write_begin,ext4:ext4_da_write_end,ext4:ext4_da_write_pages,ext4:ext4_da_write_pages_extent,ext4:ext4_direct_IO_enter,ext4:ext4_direct_IO_exit,ext4:ext4_discard_blocks,ext4:ext4_discard_preallocations,ext4:ext4_drop_inode,ext4:ext4_error,ext4:ext4_es_cache_extent,ext4:ext4_es_find_extent_range_enter,ext4:ext4_es_find_extent_range_exit,ext4:ext4_es_insert_delayed_block,ext4:ext4_es_insert_extent,ext4:ext4_es_lookup_extent_enter,ext4:ext4_es_lookup_extent_exit,ext4:ext4_es_remove_extent,ext4:ext4_es_shrink,ext4:ext4_es_shrink_count,ext4:ext4_es_shrink_scan_enter,ext4:ext4_es_shrink_scan_exit,ext4:ext4_evict_inode,ext4:ext4_ext_convert_to_initialized_enter,ext4:ext4_ext_convert_to_initialized_fastpath,ext4:ext4_ext_handle_unwritten_extents,ext4:ext4_ext_in_cache,ext4:ext4_ext_load_extent,ext4:ext4_ext_map_blocks_enter,ext4:ext4_ext_map_blocks_exit,ext4:ext4_ext_put_in_cache,ext4:ext4_ext_remove_space,ext4:ext4_ext_remove_space_done,ext4:ext4_ext_rm_idx,ext4:ext4_ext_rm_leaf,ext4:ext4_ext_show_extent,ext4:ext4_fallocate_enter,ext4:ext4_fallocate_exit,ext4:ext4_find_delalloc_range,ext4:ext4_forget,ext4:ext4_free_blocks,ext4:ext4_free_inode,ext4:ext4_fsmap_high_key,ext4:ext4_fsmap_low_key,ext4:ext4_fsmap_mapping,ext4:ext4_get_implied_cluster_alloc_exit,ext4:ext4_get_reserved_cluster_alloc,ext4:ext4_getfsmap_high_key,ext4:ext4_getfsmap_low_key,ext4:ext4_getfsmap_mapping,ext4:ext4_ind_map_blocks_enter,ext4:ext4_ind_map_blocks_exit,ext4:ext4_insert_range,ext4:ext4_invalidatepage,ext4:ext4_journal_start,ext4:ext4_journal_start_reserved,ext4:ext4_journalled_invalidatepage,ext4:ext4_journalled_write_end,ext4:ext4_load_inode,ext4:ext4_load_inode_bitmap,ext4:ext4_mark_inode_dirty,ext4:ext4_mb_bitmap_load,ext4:ext4_mb_buddy_bitmap_load,ext4:ext4_mb_discard_preallocations,ext4:ext4_mb_new_group_pa,ext4:ext4_mb_new_inode_pa,ext4:ext4_mb_release_group_pa,ext4:ext4_mb_release_inode_pa,ext4:ext4_mballoc_alloc,ext4:ext4_mballoc_discard,ext4:ext4_mballoc_free,ext4:ext4_mballoc_prealloc,ext4:ext4_nfs_commit_metadata,ext4:ext4_other_inode_update_time,ext4:ext4_punch_hole,ext4:ext4_read_block_bitmap_load,ext4:ext4_readpage,ext4:ext4_releasepage,ext4:ext4_remove_blocks,ext4:ext4_request_blocks,ext4:ext4_request_inode,ext4:ext4_shutdown,ext4:ext4_sync_file_enter,ext4:ext4_sync_file_exit,ext4:ext4_sync_fs,ext4:ext4_trim_all_free,ext4:ext4_trim_extent,ext4:ext4_truncate_enter,ext4:ext4_truncate_exit,ext4:ext4_unlink_enter,ext4:ext4_unlink_exit,ext4:ext4_write_begin,ext4:ext4_write_end,ext4:ext4_writepage,ext4:ext4_writepages,ext4:ext4_writepages_result,ext4:ext4_zero_range,filemap:file_check_and_advance_wb_err,filemap:filemap_set_wb_err,filemap:mm_filemap_add_to_page_cache,filemap:mm_filemap_delete_from_page_cache,jbd2:jbd2_checkpoint,jbd2:jbd2_checkpoint_stats,jbd2:jbd2_commit_flushing,jbd2:jbd2_commit_locking,jbd2:jbd2_commit_logging,jbd2:jbd2_drop_transaction,jbd2:jbd2_end_commit,jbd2:jbd2_handle_extend,jbd2:jbd2_handle_start,jbd2:jbd2_handle_stats,jbd2:jbd2_lock_buffer_stall,jbd2:jbd2_run_stats,jbd2:jbd2_start_commit,jbd2:jbd2_submit_inode_data,jbd2:jbd2_update_log_tail,jbd2:jbd2_write_superblock,writeback:balance_dirty_pages,writeback:bdi_dirty_ratelimit,writeback:flush_foreign, writeback:global_dirty_state,writeback:inode_foreign_history,writeback:inode_switch_wbs,writeback:sb_clear_inode_writeback,writeback:sb_mark_inode_writeback,writeback:track_foreign_dirty,writeback:wait_on_page_writeback,writeback:wbc_writepage,writeback:writeback_bdi_register,writeback:writeback_congestion_wait,writeback:writeback_dirty_inode,writeback:writeback_dirty_inode_enqueue,writeback:writeback_dirty_inode_start,writeback:writeback_dirty_page, writeback:writeback_exec,writeback:writeback_lazytime,writeback:writeback_lazytime_iput,writeback:writeback_mark_inode_dirty,writeback:writeback_pages_written,writeback:writeback_queue,writeback:writeback_queue_io,writeback:writeback_sb_inodes_requeue,writeback:writeback_single_inode,writeback:writeback_single_inode_start,writeback:writeback_start,writeback:writeback_wait,writeback:writeback_wait_iff_congested,writeback:writeback_wake_background,writeback:writeback_write_inode,writeback:writeback_write_inode_start,writeback:writeback_written"
#	Resource monitoring
resourceMonitor=false
#	Time window per sample
timeWindowSeconds=5
#	Number of samples to take (Monitored time will be: timeWindowSeconds*desiredSamples)
#desiredSamples=99999
#	Total time monitored (NOT TAKING IN CONSIDERATION TIME BETWEEN SCREENSHOTS)
timeAcumulative=0


# Server and port to push data
server="http://192.168.8.11"
port="5003"
directory="/sensor"
#mac=$( cat /sys/class/net/eth0/address | tr : _ )

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
    echo "Sending data to the server"
    res=$(curl -sk -X POST -d "$finalOutput" -H "Content-Type: application/json" "$server:$port$directory")
done

