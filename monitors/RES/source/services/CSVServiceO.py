#!/usr/bin/env python

import csv

from logger.Logger import Logger
from services.ConfigService import config
class CSVServiceO:
  log = Logger(__name__)

  def __init__(self):
    self.filename = 'evaluation' + ".csv"
    self.fieldnames = ['name', 'index', 'score']

    self.index = {}
    self.create(self.filename, self.fieldnames)
        

  def append(self, data):
    data['name'] = data['name'] + str(5)
    if not data['name'] in self.index:
      self.index[data['name']] = 0
    idx = self.index[data['name']]
    data['index'] = idx
    self.index[data['name']] = self.index[data['name']] + 1
    with open(self.filename, "a", newline="", encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
      writer.writerow(data)
  
  def create(self, filename, fieldnames):
    with open(filename, "w", newline="", encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
