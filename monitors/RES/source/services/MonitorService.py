from monitors.HardwareMonitor import HardwareMonitor
from monitors.MonitorSim import MonitorSim
from monitors.PerfMonitor import PerfMonitor
from logger.Logger import Logger
from services.CSVService import CSVService
from services.ConfigService import config

import time

class MonitorService():
  log = Logger(__name__)

  def __init__(self, policyService, rmqService = None, simulation_file = None, pause_simulation_on = None):
    self.is_simulation = simulation_file is not None
    self.pause_simulation_on = pause_simulation_on
    self.is_csv_enabled = config.get_general_config()['csvEnabled']
    self.is_rabbitMQ_enabled = config.get_general_config()['rabbitMQEnabled'] and rmqService is not None
    self.policyService = policyService

    if (self.is_simulation):
       self.sim_monitor = MonitorSim(simulation_file)
    else:
      self.hw_monitor = HardwareMonitor()
      self.perf_monitor = PerfMonitor()

    if self.is_rabbitMQ_enabled:
      self.rabbitMQService = rmqService
    if self.is_csv_enabled:
      self.csvService = CSVService(self.hw_monitor, self.perf_monitor)

  def monitor(self):
    data = { "time": int(time.time()) }

    if (not self.is_simulation):
      # Add other monitors here
      perf_data = self.perf_monitor.monitor()
      hw_data = self.hw_monitor.monitor()

      if (len(perf_data.keys()) == 0):
        time.sleep(config.get_perf_config()['monitor_window'])

      for hw_key in hw_data.keys():
        data[hw_key] = hw_data.get(hw_key)

      for perf_key in perf_data.keys():
        data[perf_key] = perf_data.get(perf_key)
      
    else:
      if (self.is_simulation):
        time.sleep(config.get_perf_config()['monitor_window'])
      sim_data = self.sim_monitor.monitor()
      if (sim_data == 0):
        return 0
      else:
        for sim_key in sim_data.keys():
          data[sim_key] = sim_data.get(sim_key)

    policies_met = self.check_policies(data)
    try: 
      self.transmit_data(data, policies_met)
    except Exception as e:
      self.log.error(e)
    try:
      self.listen_for_new_commands()
    except Exception as e:
      self.log.warn(e)
    self.write_to_csv(data)
    return data
  

  def check_policies(self, data):
    policies_met = self.policyService.check_policies(data)
    
    
    if (self.is_simulation and self.pause_simulation_on is not None):
      if (len(policies_met) > 0):
        for policy in policies_met:
          if policy["name"] in self.pause_simulation_on:
            input('Policy detected, press ENTER to continue...')
    return policies_met

  def write_to_csv(self, data):
    if (not self.is_simulation and self.is_csv_enabled):
      self.csvService.append(data)

  def transmit_data(self, data, policies_met):
    if (self.is_rabbitMQ_enabled):
      self.rabbitMQService.send_data(data, policies_met)

  def listen_for_new_commands(self):
    if (self.is_rabbitMQ_enabled):
      self.rabbitMQService.consume_next()
