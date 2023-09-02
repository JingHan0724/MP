#!/usr/bin/env python

import csv
from logger.Logger import Logger
from monitors.Monitor import AbstractMonitor
from constants import constant
from services.ConfigService import config
class MonitorSim(AbstractMonitor):

  log = Logger(__name__)

  def __init__(self, simulation_file):
    self.log.warn('Loading Simulator Monitor... (THIS IS A SIMULATION!)')
    self.index = 0
    self.example_data = constant.SIM_DATA_FOLDER + simulation_file

  def get_field_names(self):
    return [
      "cpu",
      "memory",
      "ioread",
      "iowrite",
      "ioreadbytes",
      "iowritebytes",
      "ioreadtime",
      "iowritetime",
      "iobusytime",
      "read_merge",
      "write_merge",
      "net_in",
      "net_out",
      "pkt_in",
      "pkt_out",
      "err_in",
      "err_out",
      "drop_in",
      "drop_out",
    ]

  def monitor(self):
    self.log.log('Index {}'.format(self.index))
    try:
      with open(self.example_data, "r", newline="", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        try:
          ordered_dict_from_csv = list(reader)[self.index]
          dict_from_csv = dict(ordered_dict_from_csv)
          self.index = self.index + 1
          return dict_from_csv
        except IndexError:
          self.log.log('End of simulation data reached')
          return 0
    except FileNotFoundError:
      self.log.error('Simulation data not found at {}'.format(self.example_data))
      return 0