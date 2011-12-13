import nose
import random
from sqlalchemy import engine_from_config
from datajongleur.utils.config import LoadConfig
from datajongleur.neuro.models import *
from datajongleur import initialize_sql
from datajongleur.neuro.pq_based import *

def setup_func():
  config = LoadConfig('nose.ini')
  engine = engine_from_config(config, 'sqlalchemy.')
  initialize_sql(engine)

def teardown_func():
  pass

@nose.with_setup(setup_func, teardown_func)
def test_pq_based_TimePoint():
  random_number = random.random()
  test_unit = random.choice(['s', 'ms', 'us', 'ns', 'ps'])
  tp_dto = DTOTimePoint(random_number, test_unit)
  tp = TimePoint.newByDTO(tp_dto)
  tp.save()
  l_key = tp.l_key

  tp = TimePoint(random.random(), 's')
  tp.save()

  tp = TimePoint.load(l_key)
  assert tp.units == test_unit

def test_pq_based_Period():

  
  spike_times = SpikeTimes([1.3, 1.9, 2.5], "ms")


