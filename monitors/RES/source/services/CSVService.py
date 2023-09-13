#!/usr/bin/env python

import time 
import requests

from logger.Logger import Logger
from services.ConfigService import config

field_order = ["cpu","seconds","ioread","iowrite","ioreadbytes","iowritebytes","ioreadtime","iowritetime","iobusytime","read_merge",
    "write_merge","memory","net_in","net_out","pkt_in","pkt_out","err_in","err_out","drop_in","drop_out","timer:tick_stop",
    "sched:sched_process_exec","sched:sched_waking","task:task_newtask","sched:sched_stat_runtime","timer:timer_cancel",
    "timer:timer_init","timer:timer_start","workqueue:workqueue_execute_start","branch-instructions","branch-misses","bus-cycles",
    "cache-misses","cache-references","cpu-cycles","instructions","context-switches","cpu-migrations","minor-faults",
    "page-faults","L1-dcache-load-misses","L1-dcache-loads","L1-dcache-store-misses","L1-dcache-stores","L1-icache-load-misses",
    "L1-icache-loads","LLC-load-misses","LLC-loads","LLC-store-misses","LLC-stores","branch-load-misses","branch-loads",
    "dTLB-load-misses","dTLB-store-misses","iTLB-load-misses","armv7_cortex_a7/br_immed_retired/","armv7_cortex_a7/br_mis_pred/",
    "armv7_cortex_a7/br_pred/","armv7_cortex_a7/bus_cycles/","armv7_cortex_a7/cpu_cycles/","armv7_cortex_a7/exc_return/",
    "armv7_cortex_a7/exc_taken/","armv7_cortex_a7/inst_retired/","armv7_cortex_a7/l1d_cache/","armv7_cortex_a7/l1d_cache_refill/",
    "armv7_cortex_a7/l1d_cache_wb/","armv7_cortex_a7/l1d_tlb_refill/","armv7_cortex_a7/l1i_cache/","armv7_cortex_a7/l1i_cache_refill/",
    "armv7_cortex_a7/l1i_tlb_refill/","armv7_cortex_a7/l2d_cache/","armv7_cortex_a7/l2d_cache_wb/","armv7_cortex_a7/ld_retired/",
    "armv7_cortex_a7/mem_access/","armv7_cortex_a7/pc_write_retired/","armv7_cortex_a7/st_retired/","armv7_cortex_a7/unaligned_ldst_retired/",
    "armv7_cortex_a7/cid_write_retired/","armv7_cortex_a7/bus_cycles/","block:block_bio_frontmerge","block:block_dirty_buffer",
    "block:block_split", "block:block_touch_buffer","ext4:ext4_es_lookup_extent_enter","ext4:ext4_ext_load_extent","ext4:ext4_writepages_result",
    "ext4:ext4_journal_start","filemap:mm_filemap_add_to_page_cache","jbd2:jbd2_handle_stats","ext4:ext4_da_update_reserve_space",
    "ext4:ext4_sync_file_enter","jbd2:jbd2_checkpoint_stats","ext4:ext4_free_inode","ext4:ext4_evict_inode","ext4:ext4_releasepage",
    "ext4:ext4_unlink_enter","block:block_bio_remap","filemap:mm_filemap_delete_from_page_cache","kmem:kfree","kmem:kmem_cache_alloc",
    "kmem:mm_page_alloc_zone_locked","kmem:mm_page_free","mmc:mmc_request_done","writeback:global_dirty_state","writeback:sb_clear_inode_writeback",
    "writeback:wait_on_page_writeback","napi:napi_poll","tcp:tcp_probe","net:netif_rx","gpio:gpio_value","irq:softirq_exit",
    "pagemap:mm_lru_activate","rpm:rpm_return_int","fib:fib_table_lookup","raw_syscalls:sys_enter","random:credit_entropy_bits"
]

class CSVService:
  log = Logger(__name__)
  
  def __init__(self, hw_monitor, perf_monitor, server_url):
    self.time = time.time()
    self.filename = ""
    self.fieldnames = ["time"] + field_order
    self.server_url = server_url
    self.header_sent = False
    self.check_and_send_header()
  
  def check_and_send_header(self):
    """
    Sends the header to the server as CSV using a POST request
    """
    if not self.header_sent:
      header = {field: field for field in self.fieldnames}
      response = self.send_to_server(header)

      if response.status_code == 200:
        self.header_sent = True
        print("Header sent successfully to the server.")
      else:
        print("Failed to send header. Server returned status code: {}".format(response.status_code))

  def append(self, data):
    """
    Appends data to the server as CSV using a POST request
    """
    if not self.header_sent:
      self.check_and_send_header()
    
    data["time"] = int(time.time())
    response = self.send_to_server(data)
    if response.status_code == 200:
      print("Data sent successfully to the server.")
    else:
      print("Failed to send data. Server returned status code: {}".format(response.status_code))

  def send_to_server(self, data):
    """
    Sends CSV data to the server as text using a POST request.
    """
    try:
      csv_text = ",".join([str(data[field]) for field in self.fieldnames])
      response = requests.post(self.server_url, data={"csv_data": csv_text}) 
      return response
    except Exception as e:
      print("Error sending data to the server: {}".format(str(e)))
