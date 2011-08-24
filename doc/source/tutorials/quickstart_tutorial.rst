
.. _Quantities: http://packages.python.org/quantities/index.html

====================
Quick-Start Tutorial
====================

Datajongleur is designed to handle basic scientific data. In order to stay
consistent and flexible at the same time, we implemented all classes according
to principle :ref:`interfaces`.

Getting Started
===============

A standard implementation for neuroscience is based on `Quantities`_ via
``QuantitiesAdapter`` (``datajongleur.core.quantity.QuantitiesAdapter``). Here
is a set of classes with there inheritances
(``datajongleur.neuro.pq_based.py``, see also :ref:`pq_based`):

* ``Moment(Quantity)``
* ``Period(Interval)``
* ``SampledTimeSeries(Quantity, SampledSignal, Interval)``
* ``RegularlySampledTimeSeries(SampledTimeSeries, RegularlySampledSignal)``
* ``SpikeTimes(SampledTimeSeries)``
* ``BinnedSpikes(RegularlySampledTimeSeries)``

.. testsetup:: pq_based

  from datajongleur.neuro.pq_based import *

Now let's start::

  from datajongleur.neuro.pq_based import *

``QuantitiesAdapter``
---------------------

Implements ``Quantity`` and inherits from ``Quantities``:

.. testcode:: pq_based

  from datajongleur.core.quantity import QuantitiesAdapter
  q = QuantitiesAdapter([1,2,3], 'mV')
  print q.max()
  print type(q.max())

.. testoutput:: pq_based

  3 mV
  <class 'datajongleur.core.quantity.QuantitiesAdapter'>

``Moment``
----------

Implements ``Quantity`` and inherits from ``QuantitiesAdapter``

.. testcode:: pq_based

  a = Moment(1, "ms")
  b = Moment(2, "ms")
  c = Moment(2, "ms")
  d = Moment(2, "s")
  print (a==b)
  print (b==c)
  print a + b
  print a.amount
  print a.units
  print "The amount of a + d = %s" %((a + d).amount)
  print "The units of a + d: %s" %((a + d).units)

.. testoutput:: pq_based

  False
  True
  3 ms
  1
  ms
  The amount of a + d = 2001.0
  The units of a + d: ms



``Period``
----------

Implements ``Interval``.

.. testcode:: pq_based

  p = Period(1,2,"s")
  print p.length # see interface Interval
  print p.start
  print p.stop

.. testoutput:: pq_based

  1 s
  1 s
  2 s

``SampledTimeSeries``
---------------------

Implements ``Quantity``, ``SampledSignal``, and ``Interval``.

.. testcode:: pq_based

  sts = SampledTimeSeries([1,2,3], 'mV', [1,4,7], 's')
  # Interval-methods
  print sts.length
  print sts.start
  print sts.stop
  # SampledSignal-methods
  print sts.signal
  print sts.signal_base

.. testoutput:: pq_based

  6 s
  1 s
  7 s
  [1 2 3] mV
  [1 4 7] s

``RegularlySampledTimeSeries``
-------------------------------------------------------------------------
Implements ``RegularlySampledSignal`` and inherits from ``SampledTimeSeries``.

.. testcode:: pq_based

  rsts = RegularlySampledTimeSeries([1,2,5],"mV", 1, 5, "s")
  # Interval-methods (from SampledTimeSeries)
  print rsts.length
  print rsts.start
  print rsts.stop
  # SampledSignal-methods (from SampledTimeSeries)
  print rsts.signal
  print rsts.signal_base
  # RegulartlySampledSignal-methods
  print rsts.sampling_rate
  print rsts.step_size

.. testoutput:: pq_based

  4 s
  1 s
  5 s
  [1 2 5] mV
  [ 1.  3.  5.] s
  0.5 1/s
  2.0 s

``SpikeTimes``
--------------

Inherits from ``SampledTimeSeries`` (which implements ``Quantity``,
``SampledSignal``, and ``Interval``).

.. testcode:: pq_based

  spiketimes = SpikeTimes([1.3, 1.9, 2.5], "ms")
  # Interval-methods
  print spiketimes.length
  print spiketimes.start
  print spiketimes.stop
  # SampledSignal-methods
  print spiketimes.signal
  print spiketimes.signal_base
  # all information
  print spiketimes

.. testoutput:: pq_based

  1.2 ms
  1.3 ms
  2.5 ms
  [ True  True  True] dimensionless
  [ 1.3  1.9  2.5] ms
  
  signal:          [ True  True  True] dimensionless,
  signalbase:      [ 1.3  1.9  2.5] ms,
  start:           1.3 ms,
  stop:            2.5 ms,
  length:          1.2 ms,
  n sample points: 3 dimensionless


``BinnedSpikes``
--------------------------------------------

Inherits from  ``RegularlySampledTimeSeries`` (which implements
``RegularlySampledSignal`` and inherits from ``SampledTimeSeries``

.. testcode:: pq_based

  bs = BinnedSpikes([4,3,0,2], 1, 5, "ms")
  # Interval-methods (from SampledTimeSeries)
  print bs.length
  print bs.start
  print bs.stop
  # SampledSignal-methods (from SampledTimeSeries)
  print bs.signal
  print bs.signal_base
  # RegulartlySampledSignal-methods
  print bs.sampling_rate
  print bs.step_size

.. testoutput:: pq_based

  4 ms
  1 ms
  5 ms
  [4 3 0 2] dimensionless
  [ 1.          2.33333333  3.66666667  5.        ] ms
  0.75 1/ms
  1.33333333333 ms

Links
=====

* Python Package `Quantities`_ 



