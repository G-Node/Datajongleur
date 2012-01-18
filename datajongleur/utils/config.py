"""
Source:
`<http://code.activestate.com/recipes/65334-use-good-old-ini-files-for-configuration/>`_
"""

import ConfigParser
import string

_ConfigDefault = {
    "sqlalchemy.url":            "sqlite:///test.sqlite"
    }

def LoadConfig(file, config={}):
  """
  returns a dictionary with key's of the form
  <section>.<option> and the values 
  """
  config = config.copy()
  cp = ConfigParser.ConfigParser()
  cp.read(file)
  for sec in cp.sections():
    name = string.lower(sec)
    for opt in cp.options(sec):
      config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
  return config

def connectDB(filename='db_setup.ini'):
  from sqlalchemy import engine_from_config
  from datajongleur import initialize_sql
  config = LoadConfig(filename)
  engine = engine_from_config(config, 'sqlalchemy.')
  initialize_sql(engine)
  

if __name__=="__main__":
  print LoadConfig("some.ini", _ConfigDefault)
