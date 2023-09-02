#!/usr/bin/env python
import subprocess
import re
import time
from logger.Logger import Logger
from monitors.Monitor import AbstractMonitor
from services.ConfigService import config


class PerfMonitor(AbstractMonitor):
  log = Logger(__name__)

  def __init__(self):
    self.log.log('Loading perf monitor...')
    self.old_data = []
    self.monitored_events = []

    for event_category in config.get_perf_events():
      self.monitored_events.extend(config.get_perf_events()[event_category])

    self.monitoring_frequency_seconds = config.get_perf_config()['monitor_window']
    self.perf_name = config.get_perf_config()['process']
  
  def monitor(self):
    data = self._monitor_perf()
    self._add_data_to_history(data)
    return data

  def get_field_names(self):
    return self.monitored_events

  def _monitor_perf(self):
    try:
      command = [self.perf_name, 'stat', '-e', ','.join(self.monitored_events), '-a', 'sleep', str(self.monitoring_frequency_seconds)]
      process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout_output, stderr_output = process.communicate()
    except:
      self.log.warn('Perf not available on this platform...')
      return {}

    # Wait for perf to return 
    while process.poll() is None:
      time.sleep(0.5)

    data = self._read_data(stderr_output) # Not a bug. Perf sends to stderr
    return data

  def _read_data(self,output):
    perfData = {}
    output_decoded = output.decode('utf-8')
    output_list = output_decoded.splitlines()

    for line in output_list:
      reg = re.search(r"\d*\s{2,}.*", line)
      if reg:
        matchList = reg.group(0).split()
        occurences = matchList[0]
        key = matchList[1]
        if (occurences == '<not'):
          occurences = 'nan'
          key = matchList[2]
        perfData[key] = occurences
    return perfData

  def _add_data_to_history(self, data):
    data_in_stack = len(self.old_data)
    if (data_in_stack == 3):
       self.old_data.pop(0)
    self.old_data.append(data)
