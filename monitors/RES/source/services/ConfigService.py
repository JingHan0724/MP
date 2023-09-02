import random
import string
import glob
from logger.Logger import Logger
from entities.Policy import Policy
from services.YAMLService import YAMLService
from constants import constant

class ConfigService:
  log = Logger(__name__)

  perf_events = []
  policies = []

  def __init__(self):
    self.config = self._read_yaml(constant.CONFIG_PATH)
    if (not 'deviceRndId' in self.config['general'].keys()):
      self.log.debug('Device random id does not exist, generating one...')
      self._generate_random_device_id()
    self.load_policies()

  def load_policies(self):
    self.log.debug('Loading policies...')

    policies = glob.glob(constant.POLICIES_PATH + '*.yaml') 
    policies_paths = []
    for policy in policies:
      self.log.debug("Found policy " + policy)
      policies_paths.append(policy)
    policies_objs = []
    for policy in policies_paths:
      try:
       policies_objs.append(Policy(self._read_yaml(policy)))
      except:
        self.log.warn('Skipping invalid policy...')
    self.policies = policies_objs
    
  def _read_yaml(self, filename):
    return YAMLService.read(filename)

  def _write_yaml(self, filename, content):
    return YAMLService.override(filename, content)
  
  def _get_config_section(self, section):
    try:
      return self.config[section]
    except KeyError:
      self.log.error('Malformatted config! ' + section + ' is missing')

  def get_policies(self):
    return self.policies

  def get_perf_events(self):
    return self._get_config_section('perf_events')
  
  def get_hw_events(self):
    return self._get_config_section('hw_events')
  
  def get_perf_config(self):
    return self._get_config_section('perf')

  def get_rabbitMQ_config(self):
    return self._get_config_section('rabbitMQ')
  
  def get_general_config(self):
    return self._get_config_section('general')
  
  def get_device_info(self):
    return self._get_config_section('device')

  def get_deviceId(self):
    return '{}_{}'.format(self.config['general']['deviceId'], self.config['general']['deviceRndId'])
  
  def _generate_random_device_id(self):
    self.log.log('Generating random id for device')
    chars = string.ascii_lowercase + string.digits
    randomId = ''.join(random.choice(chars) for _ in range(7))
    self.config['general']['deviceRndId'] = randomId
    self._write_yaml(constant.CONFIG_PATH, self.config)
  
config = ConfigService()