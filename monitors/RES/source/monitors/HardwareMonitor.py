#!/usr/bin/env python

import psutil
from logger.Logger import Logger
from monitors.Monitor import AbstractMonitor
from services.ConfigService import config

class HardwareMonitor(AbstractMonitor):

  log = Logger(__name__)

  def __init__(self):
    self.log.log('Loading hardware monitor...')
    self.old_data = []
    self.network_interface = config.get_device_info()['newtork_interface']
    self.monitored_events = []

    for event_category in config.get_hw_events():
      self.monitored_events.extend(config.get_hw_events()[event_category])

  def monitor_cpu(self):
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

  def monitor_mem(self):
    mem_percent = psutil.virtual_memory().percent
    return mem_percent

  def monitor_net(self):
    try:
      network_io = psutil.net_io_counters(pernic=True, nowrap=True)[self.network_interface]
      net_io_in = network_io.bytes_recv
      net_io_out = network_io.bytes_sent
      packets_sent = network_io.packets_sent
      packets_recv = network_io.packets_recv
      errin = network_io.errin
      errout = network_io.errout
      dropin = network_io.dropin
      dropout = network_io.dropout
    except:
      self.log.warn('Network interface {} not found'.format(self.network_interface))
      net_io_in = 0
      net_io_out = 0
      packets_sent = 0
      packets_recv = 0
      errin = 0
      errout = 0
      dropin = 0
      dropout = 0

    return {
      "net_in": net_io_in,
      "net_out": net_io_out,
      "pkt_in": packets_recv,
      "pkt_out": packets_sent,
      "err_in": errin,
      "err_out": errout,
      "drop_in": dropin,
      "drop_out": dropout,
    }

  def monitor_io(self):
    
    disk_io = psutil.disk_io_counters(perdisk=False, nowrap=True)
    read_count = disk_io.read_count
    write_count = disk_io.write_count
    read_bytes = disk_io.read_bytes
    write_bytes = disk_io.write_bytes

    read_time = 0
    write_time = 0
    busy_time = 0
    try: 
      read_time = disk_io.read_time
      write_time = disk_io.write_time
      busy_time = disk_io.busy_time
    except AttributeError:
      self.log.warn("io read, write, busy times not available on this platform, data set to 0")

    io_read_merge = 0
    io_write_merge = 0
    try:
      io_read_merge = disk_io.read_merged_count
      io_write_merge = disk_io.write_merged_count
    except AttributeError:
      self.log.warn("io read and write merge not available, data set to 0") 
  
    return {
      "read_count": read_count,
      "write_count": write_count,
      "read_bytes": read_bytes,
      "write_bytes": write_bytes,
      "read_merged_count": io_read_merge,
      "write_merged_count": io_write_merge,
      "read_time": read_time,
      "write_time": write_time,
      "busy_time": busy_time,
    }
  
  def get_field_names(self):
    return self.monitored_events

  def monitor(self):
    cpu = self.monitor_cpu()
    memory = self.monitor_mem()
    io = self.monitor_io()
    network = self.monitor_net()

    new_data = {}
    new_data["cpu"] = cpu
    new_data["memory"] = memory 
    new_data["ioread"] = io["read_count"] 
    new_data["iowrite"] = io["write_count"]
    new_data["ioreadbytes"] = io["read_bytes"]
    new_data["iowritebytes"] = io["write_bytes"]
    new_data["ioreadtime"] = io["read_time"]
    new_data["iowritetime"] = io["write_time"]
    new_data["iobusytime"] = io["busy_time"]
    new_data["read_merge"] = io["read_merged_count"]
    new_data["write_merge"] = io["write_merged_count"]
    new_data["net_in"] = network["net_in"]
    new_data["net_out"] = network["net_out"]
    new_data["pkt_in"] = network["pkt_in"]
    new_data["pkt_out"] = network["pkt_out"]
    new_data["err_in"] = network["err_in"]
    new_data["err_out"] = network["err_out"]
    new_data["drop_in"] = network["drop_in"]
    new_data["drop_out"] = network["drop_out"]

    data = {}
    data["cpu"] = cpu
    data["memory"] = memory 
    all_data_to_transform = [
      "ioread", 
      "iowrite",
      "ioreadtime",
      "iowritetime",
      "read_merge",
      "write_merge",
      "ioreadbytes",
      "iowritebytes",
      "iobusytime",
      "net_in",
      "net_out",
      "pkt_in",
      "pkt_out",
      "err_in",
      "err_out",
      "drop_in",
      "drop_out"
    ]

    for data_to_transform in all_data_to_transform:
      data[data_to_transform] = 1

    data_in_stack = len(self.old_data)
    if (data_in_stack > 0):
      for data_to_transform in all_data_to_transform:
        data[data_to_transform] = new_data[data_to_transform] - self.old_data[data_in_stack - 1][data_to_transform]

    if (data_in_stack == 3):
       self.old_data.pop(0)
    self.old_data.append(new_data)

    return data