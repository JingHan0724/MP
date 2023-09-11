import time
from flask import Flask, request
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer
import os
import platform

bar = ''
if platform.system() == "Linux":
    bar = "/"
elif platform.system() == "Windows":
    bar = '\\'

app = Flask(__name__)
api = Api(app)
data_directory = str(os.getcwd())

header="time,timestamp,seconds,connectivity,alarmtimer:alarmtimer_fired,alarmtimer:alarmtimer_start," \
       "block:block_bio_backmerge,block:block_bio_remap,block:block_dirty_buffer,block:block_getrq," \
       "block:block_touch_buffer,block:block_unplug,cachefiles:cachefiles_create,cachefiles:cachefiles_lookup," \
       "cachefiles:cachefiles_mark_active,clk:clk_set_rate,cpu-migrations,cs,dma_fence:dma_fence_init," \
       "fib:fib_table_lookup,filemap:mm_filemap_add_to_page_cache,gpio:gpio_value,ipi:ipi_raise," \
       "irq:irq_handler_entry,irq:softirq_entry,jbd2:jbd2_handle_start,jbd2:jbd2_start_commit,kmem:kfree," \
       "kmem:kmalloc,kmem:kmem_cache_alloc,kmem:kmem_cache_free,kmem:mm_page_alloc,kmem:mm_page_alloc_zone_locked," \
       "kmem:mm_page_free,kmem:mm_page_pcpu_drain,mmc:mmc_request_start,net:net_dev_queue,net:net_dev_xmit," \
       "net:netif_rx,page-faults,pagemap:mm_lru_insertion,preemptirq:irq_enable,qdisc:qdisc_dequeue," \
       "qdisc:qdisc_dequeue,random:get_random_bytes,random:mix_pool_bytes_nolock,random:urandom_read," \
       "raw_syscalls:sys_enter,raw_syscalls:sys_exit,rpm:rpm_resume,rpm:rpm_suspend,sched:sched_process_exec," \
       "sched:sched_process_free,sched:sched_process_wait,sched:sched_switch,sched:sched_wakeup," \
       "signal:signal_deliver,signal:signal_generate,skb:consume_skb,skb:consume_skb,skb:kfree_skb,skb:kfree_skb," \
       "skb:skb_copy_datagram_iovec,sock:inet_sock_set_state,task:task_newtask,tcp:tcp_destroy_sock,tcp:tcp_probe," \
       "timer:hrtimer_start,timer:timer_start,udp:udp_fail_queue_rcv_skb,workqueue:workqueue_activate_work," \
       "writeback:global_dirty_state,writeback:sb_clear_inode_writeback,writeback:wbc_writepage," \
       "writeback:writeback_dirty_inode,writeback:writeback_dirty_inode_enqueue,writeback:writeback_dirty_page," \
       "writeback:writeback_mark_inode_dirty,writeback:writeback_pages_written,writeback:writeback_single_inode," \
       "writeback:writeback_write_inode,writeback:writeback_written\n"

class sensor(Resource):

    def post(self, sensorid):
        vector = request.data.decode("utf-8")
        #print(vector)
        #vector = vector[:-1]
        vector = vector + "\n"
        file_path = data_directory + bar + sensorid
        append_write = 'a'  # append if already exists
        if not os.path.exists(file_path):
            file = open(file_path, append_write)
            file.write(header)
            file.close()
        file = open(file_path, append_write)
        file.write(vector)
        file.close()

        return 200


def launch_REST_Server():
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    api.add_resource(sensor, '/sensor/<sensorid>')  # Route_1
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()


if __name__ == "__main__":
    launch_REST_Server()

