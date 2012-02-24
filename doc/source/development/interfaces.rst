.. _Heise Developer (DE): http://www.heise.de/developer/artikel/Value-Object-Einsatz-228086.html

.. _Martin Fowler: http://martinfowler.com/eaaDev/quantity.html

.. _interfaces:

==========
Interfaces
==========

Datajongleur is designed to handle basic scientific data. In order to stay
consistent and flexible at the same time, we implemented all classes according
to basic interfaces.

:download:`Here: schema of core interfaces </_download/core_interfaces.pdf>`.
  
All classes are conform to fundamental interfaces. Here, ``BaseValue``
(see `Heise Developer (DE)`_)and ``BaseQuantity`` (see `Martin Fowler`_) are
the core interfaces:

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

Note: For convenience, all ``getters`` and ``setters`` are accessible via
properties (``instance.getAmount()`` -> ``instance.amount``).

.. index::
   single: interfaces; Interval
   single: Interval

.. _Interval:

``Interval``
------------

* ``start``
* ``stop``
* ``length``

.. index::
   single: interfaces; SampledSignal
   single: SampledSignal

.. _SampledSignal:

``SampledSignal``
-----------------

* ``signal``
* ``base``
* ``n_sampling_points``

.. index::
   single: interfaces; RegularlySampledSignal
   single: RegularlySampledSignal

.. _RegularlySampledSignal:

``RegularlySampledSignal`` (``SampledSignal``, ``Interval``)
------------------------------------------------------------

From ``SampledSignal``:

* ``signal``
* ``base``
* ``n_sampling_points``

From ``Interval``:

* ``start``
* ``stop``
* ``length``

Additional:

* ``sampling_rate``
* ``step_size``

Source Code
===========

``datajongleur/core/interfaces.py``:

.. literalinclude:: /../../datajongleur/beanbags/interfaces.py

Links
=====

* ``Value Objects``: `Heise Developer (DE)`_
* ``Quantity``: `Martin Fowler`_

