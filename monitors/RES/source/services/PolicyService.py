#!/usr/bin/env python

from logger.Logger import Logger
from entities.Policy import Policy
from constants import constant
from services.ConfigService import config    
import os


class PolicyService:
  log = Logger(__name__)

  def __init__(self):
    self.policies = config.get_policies()

  def check_policies(self, data):
    policies_met = []
    for policy in self.policies:
      if (policy.is_independent()):
        policies_met.extend(self.check_policy(data, policy))
    return policies_met
      
  def check_policy(self, data, policy):
    self.log.debug('CHECKING POLICY {}'.format(policy.get_name()))
    policies_met = []
    abnormal_categories = self.find_triggered_categories(policy, data)
    if (self.is_policy_met(abnormal_categories, policy)):
      policies_met.append({
        'name': policy.name,
        'categories': abnormal_categories,
      })
      for other_policy in self.policies:
        if (other_policy.is_dependent_of(policy)):
          policies_met.extend(self.check_policy(data, other_policy))
    return policies_met

  def find_triggered_categories(self, policy, data):
    abnormal_categories = []
    for category in policy.get_metrics_categories():
      self.log.verbose('    EVALUATING {} | w[{}]'.format(category, str(policy.get_weights()[category])))
      score = 0
      abnormal_metrics = self.find_triggered_metrics(policy.get_metrics()[category], data)
      for abnormal_metric in abnormal_metrics:
        score = score + abnormal_metric['score']
      if (self.is_policy_category_abnormal(abnormal_metrics, policy, category)):
        abnormal_categories.append({
          'name': category,
          'metrics': abnormal_metrics,
          'score': policy.weights[category],
        })
      self.log.verbose('    total score of {}/100'.format(str(score)))
    return abnormal_categories

  def find_triggered_metrics(self, metrics, data):
    abnormal_metrics = []
    for metric in metrics:
      for data_key in data.keys():
        if (metric.meets_condition(data[data_key], data_key)):
          abnormal_metrics.append({
            'name': metric.get_name(),
            'value': data[data_key],
            'score': metric.get_weight()
          })
    return abnormal_metrics

  def is_policy_met(self, abnormal_categories, policy):
    score = 0
    for abnormal_category in abnormal_categories:
      score = score + abnormal_category['score']
    self.log.debug('Score {}'.format(score))
    if (score >= 500):
      self.log.verbose('    !!! Policy {} is met. Score {}'.format(policy.get_name(), score))
      is_met = True;
    else:
      self.log.verbose('    Policy {} is NOT met. Score: {}'.format(policy.get_name(), score))
      is_met = False
    self.log.log('{} - {}'.format(policy.get_name(), score))
    return is_met
    

  def is_policy_category_abnormal(self, abnormal_metrics, policy, category):
    metrics_in_category = len(policy.get_metrics()[category])
    if (metrics_in_category == 0):
      return True
    score = 0
    for abnormal_metric in abnormal_metrics:
      score = score + abnormal_metric['score']
    self.log.debug('Score {} -> {}'.format(category, score))
  
    if (score >= 100.0):
      return True
    else:
      return False
  
  def create_policy(self, policy):
    try:
      new_policy = Policy(policy)
    except ValueError as e:
      return {"success": False, "error": "BAD_REQUEST", 'message': str(e)}
    except:
      self.log.warn('Error while creating policy...')
      return {"success": False, "error": "UNKNOWN"}
    for existingPolicy in self.policies:
      if new_policy.get_name() == existingPolicy.get_name():
          return {"success": False, "error": "EXISTING", 'message': 'Policy already exist!'}
    try:
      new_policy.save()
      config.load_policies()
      self.policies = config.get_policies()
      return {"success": True}
    except:
        return {"success": False, "error": "UNKNOWN"}


  def edit_policy(self, policy_name, policy):
    try:
      for existingPolicy in self.policies:
        if policy_name == existingPolicy.get_name():
          try:
            edited_policy = Policy(policy)
            edited_policy.save()
            config.load_policies()
            self.policies = config.get_policies()
            return {"success": True}
          except ValueError as e:
            return {"success": False, "error": "BAD_REQUEST", 'message': str(e)}
          except:
            self.log.warn('Error while updating policy...')
            return {"success": False, "error": "UNKNOWN"}
      return {"success": False, "error": "NOT_EXISTING", 'message': 'Policy {} does not exist'.format(policy_name)}
    except ValueError as e:
      return {"success": False, "error": "BAD_REQUEST", 'message': str(e)}
    except:
      return {"success": False, "error": "UNKNOWN", 'message': 'unkown error'}

  def delete_policy(self,  policy_name):
    for existingPolicy in self.policies:
      if policy_name == existingPolicy.get_name():
        try:
          os.remove('{}{}.yaml'.format(constant.POLICIES_PATH, policy_name))
          config.load_policies()
          self.policies = config.get_policies()
          return {"success": True}
        except Exception as e:
            self.log.warn('Error while deleting policy...')
            return {"success": False, "error": "UNKNOWN", 'message': str(e)}
    return {"success": False, "error": "NOT_EXISTING", 'message':  'Policy {} does not exist'.format(policy_name)}
