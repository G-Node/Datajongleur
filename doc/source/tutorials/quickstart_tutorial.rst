.. _Heise Developer (DE): http://www.heise.de/developer/artikel/Value-Object-Einsatz-228086.html

.. _Martin Fowler: http://martinfowler.com/eaaDev/quantity.html

.. _Quantities: http://packages.python.org/quantities/index.html

====================
Quick-Start Tutorial
====================

Datajongleur is designed to handle basic scientific data.

Interfaces
==========

All classes are conform to fundamental interfaces. Here, ``BaseValue``
(see `Heise Developer (DE)`_)and ``BaseQuantity`` (see `Martin Fowler`_)are the core interfaces:

* ``BaseValue`` has the following properties:

  * immutable
  * operation on BaseValue-objects return new BaseValue-objects
  * "==" depends on object-values and not on object-identity
  * a hash is calculted by object-values

* a ``Quantity`` has the following behavior:

  * ``getAmount``
  * ``getunits``
  * +, -, * , /, <, >, ==

Three more interfaces resemble the nature of measurements:

* ``Interval``
* ``SampledSignal``
* ``RegularlySampledSignal``

For an overview see

* :download:`core interfaces </_download/core_interfaces.pdf>`.
  
Note: For convenience, all ``getters`` and ``setters`` are accessible via
properties (``instance.getAmount()`` -> ``instance.amount``).

Getting Started
===============

A standard implementation for neuroscience is based on `Quantities`_ via
``datajongleur.core.quantity.QuantitiesAdapter``. Here is a
set of classes with there inheritances (``datajongleur.neuro.pq_based.py``):

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


Try:

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

To get:

.. testoutput:: pq_based

  False
  True
  3 ms
  1
  ms
  The amount of a + d = 2001.0

Links
=====

* ``Value Objects``: `Heise Developer (DE)`_
* ``Quantity``: `Martin Fowler`_
* Python Package `Quantities`_ 



