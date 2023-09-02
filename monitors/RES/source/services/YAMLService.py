#!/usr/bin/env python

import yaml

class YAMLService:
    
  @staticmethod
  def read(filename):
    with open(filename, 'r', encoding='utf-8') as stream:
      try:
        return yaml.safe_load(stream)
      except yaml.YAMLError as exc:
        raise RuntimeError('Failed to open YAML file ' + filename)

  @staticmethod
  def override(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
      yaml.dump(content, file)
