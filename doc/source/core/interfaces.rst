.. _Heise Developer (DE): http://www.heise.de/developer/artikel/Value-Object-Einsatz-228086.html

.. _Martin Fowler: http://martinfowler.com/eaaDev/quantity.html

.. _interfaces:

==========
Interfaces
==========

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

For an overview see

* :download:`core interfaces </_download/core_interfaces.pdf>`.
  
Note: For convenience, all ``getters`` and ``setters`` are accessible via
properties (``instance.getAmount()`` -> ``instance.amount``).

Source Code
===========

``datajongleur/core/interfaces.py``:

.. literalinclude:: /../../datajongleur/core/interfaces.py

Links
=====

* ``Value Objects``: `Heise Developer (DE)`_
* ``Quantity``: `Martin Fowler`_

