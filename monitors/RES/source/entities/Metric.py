#!/usr/bin/env python
import math
from logger.Logger import Logger
from constants import constant


class Metric:
  log = Logger(__name__)
  properties = [ '_id', 'name', 'condition', 'value', 'weight']

  def __init__(self, metric, metrics_length):
    try:
      self.weight = metric["weight"]
    except KeyError:
      self.weight = 100 / math.ceil(metrics_length)
    self._verify_metric(metric)
    self.name = metric["name"]
    self.condition = metric["condition"]
    self.value = metric["value"]
      
  def _verify_metric(self, raw_metric):
    for proprty in self.properties:
      if proprty not in raw_metric:
        if proprty == 'weight' or proprty == '_id':
          pass
        else:
          self.log.error('Malformatted Metric! Property {} is missing'.format(proprty))
          raise ValueError('Missing property in Metric')
    for proprty in raw_metric:
      if (proprty not in self.properties):
        self.log.error('Metric {} has invalid property {}'.format(raw_metric['name'], proprty))
        raise ValueError('Invalid property in Metric')

  def get_name(self):
    return self.name
  
  def get_condition(self):
    return self.condition

  def get_value(self):
    return self.value

  def get_weight(self):
    return self.weight
  
  def meets_condition(self, data, key):
    condition_met = False
    if (not key == self.name):
      return False
    if (self.condition == constant.IN):
      condition_met = float(data) > float(self.value[0]) and float(data) < float(self.value[1])
    elif (self.condition == constant.OUT):
      condition_met = float(data) < float(self.value[0]) or float(data) > float(self.value[1])
    elif (self.condition == constant.ABOVE):
      condition_met = float(data) >= float(self.value)
    elif (self.condition == constant.BELOW):
      condition_met = float(data) <= float(self.value)
    else:
      self.log.warn('INVALID CONDITION {} - Valid conditions are: {}, {}, {}, {}'.format(self.condition, constant.IN, constant.OUT, constant.ABOVE, constant.BELOW))
      condition_met = False
  
    self.log.verbose('            [{}] {} | w[{}] | got {} | policy {} {}'.format(condition_met, self.name, self.weight, data, self.condition, self.value))
    return condition_met
  
  def to_json(self):
    json_metric = {
      'name': self.name,
      'condition': self.condition,
      'value': self.value,
      'weight': self.weight,
     }
    return json_metric