#!/usr/bin/env python

import signal
import sys
import argparse
from services.ConfigService import config
from logger.Logger import Logger
from services.MonitorService import MonitorService
from services.RabbitMQService import RabbitMQService
from helpers.ASCII_art import print_intro
from services.PolicyService import PolicyService

class Main():
  log = Logger(__name__)

  rabbitMQService = None
  csvService = None
  monitor = True

  def __init__(self, simulation = None, pause_simulation_on = None):
    self.is_simulation = simulation is not None
    signal.signal(signal.SIGINT, self.signal_handler)
    self.policyService = PolicyService()
    if (config.get_general_config()['rabbitMQEnabled']):
      self.rabbitMQService = RabbitMQService(self.policyService)    
    self.monitorService = MonitorService(self.policyService, rmqService=self.rabbitMQService, simulation_file=simulation, pause_simulation_on=pause_simulation_on)

  def main(self):
    self.log.log("Starting Monitoring Process")
    self.log.log('Device ID: {}'.format(config.get_deviceId()))
    print_intro(self.log)
    self.start()
  
  def graceful_shutdown(self):
    self.log.log('Shutting down...')
    self.monitor = False
    if (config.get_general_config()['rabbitMQEnabled'] and self.rabbitMQService is not None):
      self.log.debug('Closing RabbitMQ connection...')
      self.rabbitMQService.closeConnection()
    sys.exit(0)

  def signal_handler(self, sig, frame):
    self.graceful_shutdown()

  def start(self):
    while self.monitor:
      self.log.verbose('Measuring...')
      data = self.monitorService.monitor()
      if (data == 0):
        self.monitor = False
    self.log.log('END')
    self.graceful_shutdown()
   
if __name__ == "__main__":  
  parser = argparse.ArgumentParser()
  parser.add_argument('--simulation', help='Start a simulation', metavar='DataFile.csv', type=str)
  parser.add_argument('--pause_sim_on', type=str, nargs='*',
                    help='List of policies names which will pause the simulation when triggered (e.g. --pause_sim_on abnormal ransomware ). Not providing any argument (i.e. --pause_sim_on) will pause at every policy that triggers. No effect without --simulation DataFile.csv')
  args = parser.parse_args()

  if (args.simulation):
    Main(args.simulation, args.pause_sim_on).main()
  else:
    Main(args.simulation).main()
