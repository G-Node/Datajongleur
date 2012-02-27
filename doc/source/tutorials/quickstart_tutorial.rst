.. _Quantities: http://packages.python.org/quantities/index.html
.. _InfoArray: http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#simple-example-adding-an-extra-attribute-to-ndarray

.. _quickstart_tutorial:

====================
Quick-Start Tutorial
====================

This quickstart tutorial focusses on the ``quantities.Quantity``-implementation
(= ``pq_based`` modules). For information abount ``quantities.Quantity`` see
http://packages.python.org/quantities/user/tutorial.html.

Getting Started
===============

Now let's start. In order to initialize a test-database use the following
lines:

.. testcode:: pq_based

  import datajongleur as dj
  from datajongleur.beanbags.neuro.pq_based import *
  session = dj.get_session()

If you run this for the first time in your working directory, ``datajongleur``
will tell you that it had to create a default configuration file
``datajongleur.ini`` (more information about this: :ref:`configuration_file`).

Note: ``session = dj.get_session()`` has to be called after importing other
modules from datajongleur. The ``session``-object is needed to connect to the
database (by default it will be a SQLite database which is stored as a file
``datajongleur.sqlite`` in your working directory).


``InfoQuantity``
----------------

``InfoQuantity`` is the most basic class of datajongleurs that underlies
``beanbags``.  Dependent on the implementation it inherits from an basic
numerical class. In the modul ``pq_based``, the underlying numercal class is
``quantities.Quantity`` which adds to ``numpy.ndarray`` a magnitude and is is
designed to handle arithmetic and conversions of physical quantities. Moreover,
a dictionary ``info`` is added (for technical background, see numpy's
`InfoArray`_):

.. testcode:: pq_based

  iq = InfoQuantity([1,2.5,3], 'ms',
    info={'author': 'Mustermann', 'age':13})

You can ``save`` and ``load`` like this:

.. testcode:: pq_based

  iq.save() # assigns an Universally Unique Identifier ``uuid`` and stores 
            # ``iq`` to the database
  uuid = iq.uuid
  iq2 = InfoQuantity.load(uuid)

Now, the ``InfoQuantity`` looks like this:

.. testcode:: pq_based

  print iq2

.. testoutput:: pq_based

  >>> InfoQuantity <<<
  array([ 1. ,  2.5,  3. ]) * ms

  Info-Attributes:
   age: 13
   author: 'Mustermann'

``info`` is stored as an attribute of the same name:

.. testcode:: pq_based

   iq2.info['age'] = 17
   print iq.info

.. testoutput:: pq_based

   {'age': 17, 'author': 'Mustermann'}
 
All arithmetics are realized with underlying ``quantities.Quantity``:

.. testcode:: pq_based

   print iq + iq
   print type(iq + iq)

.. testoutput:: pq_based

   [ 2.  5.  6.] ms
   <class 'quantities.quantity.Quantity'>

For convenience, all ``InfoQuantity``-objects offer two attributes in order to
access ``amount`` and ``units`` of its instanz.

.. testcode:: pq_based

  print iq.amount
  print iq.units

.. testoutput:: pq_based

  [ 1.   2.5  3. ]
  ms

Beanbags
========


Thats it. Now let's juggle the beanbags.

Beanbags are restricted ``InfoQuantities`` that represent standard data
objects. This standartization affects two things:

**1. the structure of** ``info`` **is fixed:**

* ``TimePoint``

  * ``info={'signal': Quantity}``

* ``Period``

  * ``info={'signal': Quantity}``

* ``SampledTimeSeries``
  
  * ``info={'signal': Quantity, 'signal_base': Quantity}``

* ``SpikeTimes``

  * ``info={'signal': Quantity, 'signal_base': Quantity}``

* ``RegularlySampledTimeSeries``

  * ``info={'signal': Quantity, 'signal_base': Quantity, 'start': Quantity,
    'stop': Quantity}``

* ``BinnedSpikes``

  * ``info={'signal': Quantity, 'signal_base': Quantity, 'start': Quantity,
    'stop': Quantity}``

**2.** *properties* **help to access different aspects of** ``info`` **:**

.. image:: /_download/neuro_beanbags.png

``TimePoint``
-------------

As beanbags are associated with a database it is easy to ``save`` and ``load``
individual beanbags:

.. testcode:: pq_based

   tp1 = TimePoint(1.0, "ms")
   tp1.save()

You need the ``uuid`` to ``load`` a stored object again:

.. testcode:: pq_based

   uuid = tp1.uuid
   tp3 = TimePoint.load(uuid)
   print type(tp3)
   print tp3

.. testoutput:: pq_based

   <class 'datajongleur.beanbags.neuro.pq_based.TimePoint'>
   >>> TimePoint <<<
   array(1.0) * ms
   
   Info-Attributes:
    signal: array(1.0) * ms

Beanbags are ``ValueObjects``. This means that comparison is not comparing the
object reference but the content of the object:

.. testcode:: pq_based
  
   tp2 = TimePoint(2.0, "ms")
   print (tp1 + tp1)
   print (tp1 + tp1) == tp2
 
.. testoutput:: pq_based

   2.0 ms
   True

``Period``
----------

Implements :ref:`Interval` (properties `start`, `stop`, and `length`):

.. testcode:: pq_based

   p = Period([2,5],"s")
   print p.start
   print p.stop
   print p.length
   print p[0]

.. testoutput:: pq_based

   2 s
   5 s
   3 s
   2 s

``SampledTimeSeries``
---------------------

Implements :ref:`Interval` (properties: ``start``, ``stop``, and ``length``)
and :ref:`SampledSignal` (properties: ``signal``, ``base``, and
``n_sampling_points``):

.. testcode:: pq_based

   sts = SampledTimeSeries([1,2,3], 'mV',
     signal_base_amount = [1,4,7],
     signal_base_units = 's')
   # Interval-properties
   print sts.start
   print sts.stop
   print sts.length
   # SampledSignal-properties
   print sts.signal
   print sts.signal_base

.. testoutput:: pq_based

   1 s
   7 s
   6 s
   [1 2 3] mV
   [1 4 7] s

``RegularlySampledTimeSeries``
------------------------------

Implements :ref:`RegularlySampledSignal` (properties: ``signal``, ``base``,
``n_sampling_points``, ``start``, ``stop``, ``length``, ``sampling_rate``,
``step_size``)

.. testcode:: pq_based

   rsts = RegularlySampledTimeSeries([1,2,5],"mV",
     start=1,
     stop=5,
     time_units="s")
   # Interval-methods (from SampledTimeSeries)
   print rsts.start
   print rsts.stop
   print rsts.length
   # SampledSignal-methods (from SampledTimeSeries)
   print rsts.signal
   print rsts.signal_base
   # RegulartlySampledSignal-methods
   print rsts.sampling_rate
   print rsts.step_size

.. testoutput:: pq_based

   1 s
   5 s
   4 s
   [1 2 5] mV
   [ 1.  3.  5.] s
   0.5 1/s
   2.0 s

``SpikeTimes``
--------------

Implements :ref:`Interval` (properties: ``start``, ``stop``, and ``length``)
and :ref:`SampledSignal` (properties: ``signal``, ``base``, and
``n_sampling_points``):

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
   print '\n', spiketimes

.. testoutput:: pq_based

   1.2 ms
   1.3 ms
   2.5 ms
   [ True  True  True] dimensionless
   [ 1.3  1.9  2.5] ms

   >>> SpikeTimes <<<
   array([ 1.3,  1.9,  2.5]) * ms
 
   Info-Attributes:
    signal: array([ True,  True,  True], dtype=bool) * dimensionless
    signal_base: array([ 1.3,  1.9,  2.5]) * ms
 
``BinnedSpikes``
----------------

Inherits from  ``RegularlySampledTimeSeries`` (which implements
``RegularlySampledSignal`` and inherits from ``SampledTimeSeries``

.. testcode:: pq_based

   bs = BinnedSpikes([4,3,0,2],
     start=1,
     stop=5,
     time_units="ms")
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
* `InfoArray`_
 
