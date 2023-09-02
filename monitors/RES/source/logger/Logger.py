import sys
import time
from services.YAMLService import YAMLService
from constants import constant
class Logger:

  colors = {
    'verbose': '\033[96m',
    'debug': '\u001b[35m',
    'log': '\033[92m',
    'warn': '\033[93m',
    'error': '\033[91m',
    'end': '\033[0m',
  }

  allLevels = ['verbose', 'debug', 'log', 'warn', 'error']

  logLevels = {
    'verbose': allLevels[-5:],
    'debug': allLevels[-4:],
    'log':  allLevels[-3:],
    'warn': allLevels[-2:],
    'error': allLevels[-1:],
  }

  yamlService = YAMLService()

  def __init__(self, context):
    self.context = context
    config = YAMLService.read(constant.CONFIG_PATH)
    self.logLevel = 'debug'
    try:
      logLevel = config['general']['logLevel']
      if (logLevel in self.allLevels):
        self.logLevel = logLevel
    except KeyError:
      self.logLevel = 'debug'

  def getTime(self):
    t = time.localtime()
    return time.strftime('%Y-%m-%d %H:%M:%S', t)
    
  def verbose(self, message):
    self.printStdOut('verbose', message)

  def debug(self, message):
    self.printStdOut('debug', message)

  def log(self, message):
    self.printStdOut('log', message)

  def warn(self, message):
    self.printStdOut('warn', message)

  def error(self, message):
      self.printStdErr('error', message)

  def printStdOut(self, level, message):
    if (level in self.logLevels[self.logLevel]):
      msg = '{}{}  [{}] - [{}]: {}{}\n'.format(self.colors[level], self.getTime(), level.upper(), self.context, message, self.colors['end']).encode('ascii', 'ignore').decode('ascii')
      sys.stdout.write(msg)
      #f = open("log.log", "a")
      # f.write(msg)
      #f.close()


  def printStdErr(self, level, message):
    # Always print error
    msg = '{}{}  [{}] - [{}]: {}{}\n'.format(self.colors[level], self.getTime(), level.upper(), self.context, message, self.colors['end']).encode('ascii', 'ignore').decode('ascii')
    sys.stderr.write(msg)
