"""
Source:
`<http://code.activestate.com/recipes/65334-use-good-old-ini-files-for-configuration/>`_
"""
import string
import os, shutil
import ConfigParser

INI_FILE_NAME = 'datajongleur.ini'
MODULE_PATH = os.path.split(__file__)[0]
INI_FULL_FILE_NAME_DEFAULT = os.path.join(MODULE_PATH, INI_FILE_NAME)

class ConfigJongleur(object):
  def __init__(
      self,
      current_ini=INI_FILE_NAME,
      default_ini=INI_FULL_FILE_NAME_DEFAULT):
    self.ensureFile(current_ini, default_ini)
    self.config = self.loadConfig(current_ini)

  def ensureFile(self, filename, default_filename):
    if not os.path.exists(filename):
      import textwrap
      information = """
        There was no file `%s` in the working directory. Creating the default
        one from `%s`.""" %(filename, default_filename)
      print (textwrap.dedent(information))
      shutil.copy(default_filename, ".")
    return

  def loadConfig(self, filename=INI_FILE_NAME, config={}):
    """
    returns a dictionary with key's of the form
    <section>.<option> and the values 
    """
    config = config.copy()
    cp = ConfigParser.ConfigParser()
    cp.read(filename)
    for sec in cp.sections():
      name = string.lower(sec)
      for opt in cp.options(sec):
        config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
    return config

if __name__=="__main__":
  cj = ConfigJongleur()
  print cj.config
