#!/usr/bin/env python
from logger.Logger import Logger
from entities.Metric import Metric
from services.YAMLService import YAMLService
from constants import constant

class Policy:
  log = Logger(__name__)

  def __init__(self, policy):
    self._verify_policy(policy)
    self.name = policy["name"]
    self.depends_on = policy["depends_on"]
    self.metrics = {
      'cpu': [Metric(m, len(self._convert_empty_metric_category('cpu', policy))) for m in self._convert_empty_metric_category('cpu', policy)],
      'memory': [Metric(m, len(self._convert_empty_metric_category('memory', policy))) for m in self._convert_empty_metric_category('memory', policy)],
      'io': [Metric(m, len(self._convert_empty_metric_category('io', policy))) for m in self._convert_empty_metric_category('io', policy)],
      'network': [Metric(m, len(self._convert_empty_metric_category('network', policy))) for m in self._convert_empty_metric_category('network', policy)],
      'others':[Metric(m, len(self._convert_empty_metric_category('others', policy))) for m in self._convert_empty_metric_category('others', policy)],
    }

    self.weights = policy["weights"]
  
  def _verify_policy(self, raw_policy):
    properties = ['name', 'depends_on', 'metrics', 'weights']
    categories = ['cpu', 'memory', 'io', 'network', 'others']
    for proprty in properties:
      if proprty not in raw_policy:
        self.log.error('Malformatted Policy! Property {} is missing'.format(proprty))
        raise ValueError('Malformatted Policy! Property {} is missing'.format(proprty))
    for proprty in raw_policy:
      if (proprty not in properties):
        self.log.error('Policy {} has invalid property {}'.format(raw_policy['name'], proprty))
        raise ValueError('Policy {} has invalid property {}'.format(raw_policy['name'], proprty))

    for category in categories:
      if category not in raw_policy['metrics']:
        self.log.error('Malformatted Policy! Category {} is missing from metrics'.format(category))
        raise ValueError('Missing category from metrics')

  def _convert_empty_metric_category(self, metric_category, raw_policy):
    if (raw_policy['metrics'][metric_category] is None):
      return []
    return raw_policy['metrics'][metric_category]

  def get_name(self):
    return self.name
  
  def is_dependent_of(self, other_policy):
    return other_policy.get_name() == self.depends_on

  def get_metrics(self):
    return self.metrics

  def get_metric_category(self, category):
    return self.metrics[category]

  def is_independent(self):
    return self.depends_on is None
  
  def get_metrics_categories(self):
    categories = []
    for metric in self.metrics:
      if (self.metrics[metric] is not None):
        categories.append(metric)
    return categories
  
  def get_weights(self):
    return self.weights
  
  def to_json(self):
    jsonPolicy = {
      'name': self.name,
      'depends_on': self.depends_on,
      'metrics': {
        'cpu': [m.to_json() for m in self.get_metric_category('cpu')],
        'memory': [m.to_json() for m in self.get_metric_category('memory')],
        'io': [m.to_json() for m in self.get_metric_category('io')],
        'network': [m.to_json() for m in self.get_metric_category('network')],
        'others': [m.to_json() for m in self.get_metric_category('others')],
      },
      'weights': self.weights,
     }
    return jsonPolicy
  
  def save(self):
    return YAMLService.override(constant.POLICIES_PATH + self.name + '.yaml', self.to_json())