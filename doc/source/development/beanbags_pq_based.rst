=====================
``beanbags.pq_based``
=====================

``InfoQuantity``
================

Look at the following ``__new__``-method:

.. code-block:: python
   :emphasize-lines: 3
   :linenos:
  
   def __new__(cls, data, units='', dtype=None, copy=True, *args, **kwargs):
     obj = cls.__base__.__new__(
         cls.__base__,
         data,
         units=units,
         dtype=dtype,
         copy=copy).view(cls)
     obj.setflags(write=False) # Immutable
     return obj

The new object has to be *initialized* with ``cls.__base__`` in order to allow a
``quantities.Quantity`` as a parameter:

.. code-block:: python

   import quantities as pq
   q = pq.Quantity([1,2,3], 'mV')
   iq = InfoQuantity(q, info={})
