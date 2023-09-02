#!/usr/bin/env python

import csv
import time 
import datetime 
import os 

from logger.Logger import Logger
from services.ConfigService import config
class CSVService:
  log = Logger(__name__)
  
  def __init__(self, hw_monitor, perf_monitor):
    self.time = time.time()
    self.filename = ""
    self.fieldnames = ["time"]
    for hw_field_name in hw_monitor.get_field_names():
      self.fieldnames.append(hw_field_name)
    for perf_field_name in perf_monitor.get_field_names():
      self.fieldnames.append(perf_field_name)
    self.create()
        

  def append(self, data):
    """
    Appends data to the .csv
    """
    with open(self.filename, "a", newline="", encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
      writer.writerow(data)
  
  def create(self):
    """
    Creates a new .csv file
    """
    self.filename = "/tmp/monitors/RES/RES_{}".format(time.time()) + ".csv"
    with open(self.filename, "w", newline="", encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
      writer.writeheader()
