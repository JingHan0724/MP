#!/usr/bin/env python
from datetime import datetime
import pika
import json
from logger.Logger import Logger
from constants import constant
from services.ConfigService import config

class RabbitMQService:
  log = Logger(__name__)

  def __init__(self,  policyService):
    self.log.log('Starting RabbitMQ service...')
    self.rmqConfig = config.get_rabbitMQ_config()
    self.policyService = policyService
    self.connection = self.setup_connection()
    self.channel = self.connection.channel()
    self.create_queues(self.channel)
    self.create_consumer()
    self.declare_device()
  
  def reset_connection(self):
    try:
      self.connection = self.setup_connection()
      self.channel = self.connection.channel()
      self.create_queues(self.channel)
      self.create_consumer()
    except Exception as e:
      self.log.error(e)
  
  def create_queues(self, channel):
    channel.queue_declare(queue='data', durable=True)
    channel.exchange_declare(exchange='monitoring', exchange_type='direct', durable=True)
    channel.queue_bind(exchange='monitoring',
                   queue='data',
                   routing_key='data')
    
    channel.queue_declare(queue='deviceDeclare', durable=True)
    channel.exchange_declare(exchange='monitoring', exchange_type='direct', durable=True)
    channel.queue_bind(exchange='monitoring',
                   queue='deviceDeclare',
                   routing_key='deviceDeclare')

  def consume_next(self):
    self.log.verbose('Checking new RabbitMQ messages...')
    has_messages = True
    while has_messages:
      try:
        method_frame, header_frame, body = self.channel.basic_get(config.get_deviceId())
      except Exception as e:
        self.log.error(e)
        pass
      if method_frame == None or method_frame.NAME == 'Basic.GetEmpty':
        self.log.verbose("No new messages")
        has_messages = False
      else:            
        json_message = body.decode('utf8')
        json_body = json.loads(json_message)
        try:
          self.log.verbose("New message found..." + json_body['cmd'])
          msg = {'code': 200, 'msg': 'ok'}
          if(json_body['cmd'] == constant.CREATE_POLICY):
            result = self.policyService.create_policy(json_body['data']['policy'])
            self.declare_device()
            msg = self.get_return_msg(result, 201)
          elif(json_body['cmd'] == constant.EDIT_POLICY):
            result = self.policyService.edit_policy(json_body['data']['name'], json_body['data']['policy'])
            self.declare_device()
            msg = self.get_return_msg(result)
          elif(json_body['cmd'] == constant.DELETE_POLICY):
            result = self.policyService.delete_policy(json_body['data']['policy'])
            self.declare_device()
            msg = self.get_return_msg(result)
          elif(json_body['cmd'] == constant.DECLARE_DEVICE):
            self.declare_device()
          else:
            self.log.warn('Invalid command received ' + json_body['msg'] )
        except Exception as e:
          self.log.warn('Error while digesting message from rabbitMQ: {}'.format(e))
          msg = {'code': 500, 'msg': 'FATAL ERROR'}
        try:
          self.channel.basic_publish(exchange = '', routing_key=header_frame.reply_to, properties=pika.BasicProperties(correlation_id = header_frame.correlation_id), body=json.dumps(msg))
          self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
          self.log.warn('RabbitMQ Error: {}'.format(e))
  
  def get_return_msg(self, result, code = 200):
    if result['success']:
      return {'code': code, 'msg': 'ok'}
    if result['error'] == 'NOT_EXISTING':
      return {'code': 404, 'msg': result['message']}
    elif result['error'] == 'NOT_EXISTING':
      return {'code': 404, 'msg': result['message']}
    else:
      return {'code': 500, 'msg': result['message']}

  def create_consumer(self, retry = False):
    try: 
      self.channel.exchange_declare(exchange=config.get_deviceId(), exchange_type='direct', durable=True)
      self.channel.queue_declare(queue=config.get_deviceId(), durable=True, exclusive=False)
      self.channel.queue_bind(exchange=config.get_deviceId(), queue=config.get_deviceId(), routing_key=config.get_deviceId())
    except Exception as e:
      if not retry:
        self.log.warn('Error while creating rabbitMQ consumer, attempting to delete the exchange and retry...')
        self.channel.queue_delete(queue=config.get_deviceId())
        self.channel.exchange_delete(exchange=config.get_deviceId())
        self.create_consumer(True)
      


  def setup_connection(self):
    try: 
      credentials = pika.PlainCredentials(self.rmqConfig['user'], self.rmqConfig['password'])
      connectionParameters = pika.ConnectionParameters(self.rmqConfig['host'], self.rmqConfig['port'], '/', credentials)
      return pika.BlockingConnection(connectionParameters)
    except Exception as e:
      self.log.error(e)

  def send_data(self, data, policies):
    deviceId = config.get_deviceId()
    messageDict = {
      'deviceID': deviceId,
      'data': data,
      'policies': policies,
      'timestamp': int(datetime.now().strftime("%s%f"))/1000, # todo: create timestamp when data is collected
    }
    try:
      return self.sendMessageToQueue('data', json.dumps(messageDict))
    except Exception as e:
      self.log.error(e)
      self.reset_connection()

  def declare_device(self):
    deviceId = config.get_deviceId()
    encodedPolicies = []
    for policy in config.get_policies():
      encodedPolicies.append(policy.to_json())

    messageDict = {
      'deviceID': deviceId,
      'data': {
        'events': {
          'perf': config.get_perf_events(),
          'hw': config.get_hw_events(),
        },
        'policies': encodedPolicies,
        'config': {
          'monitor_window': config.get_perf_config()['monitor_window'] * 1000
        }
      }
    }
    return self.sendMessageToQueue('deviceDeclare', json.dumps(messageDict))


  def sendMessageToQueue(self, queue, message):
    return self.channel.basic_publish(
      exchange='monitoring',
      routing_key=queue,
      body=message
    )

  def closeConnection(self):
    self.log.log("Closing rabbitMQ connection")
    self.connection.close()
