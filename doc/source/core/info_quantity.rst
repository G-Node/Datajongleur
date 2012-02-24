.. _InfoArray: http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#simple-example-adding-an-extra-attribute-to-ndarray

.. index::
   single: InfoQuantity
   single: Beanbags; InfoQuantity

.. _info_quantity:

============
InfoQuantity
============

(see also :ref:`quickstart_tutorial`)

``InfoQuantity`` is the most basic class of datajongleurs that underlies
``beanbags``.  Dependent on the implementation it inherits from an basic
numerical class. In the modul ``pq_based``, the underlying numercal class is
``quantities.Quantity`` which adds to ``numpy.ndarray`` a magnitude and is is
designed to handle arithmetic and conversions of physical quantities. Moreover,
a dictionary ``info`` is added (for technical background, see numpy's
`InfoArray`_):

.. testcode:: pq_based

  import datajongleur as dj
  from datajongleur.beanbags.neuro.pq_based import *
  session = dj.get_session()

  iq = InfoQuantity([1,2.5,3], 'ms', info={'author': 'Mustermann', 'age':13})
  iq.save() # assigns an Universally Unique Identifier `uuid` and stores the
            # InfoQuantity to the database
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
 
All arithmetics work directly with underlying ``quantities.Quantity``:

.. testcode:: pq_based

   print iq + iq
   print type(iq + iq)

.. testoutput:: pq_based

   [ 2.  5.  6.] ms
   <class 'quantities.quantity.Quantity'>

Initialize with kwargs
======================

Instead of passing an info-dict as argument you can also use key words:

.. testcode:: pq_based

   iq = InfoQuantity([1,2.5,3], 'ms', author='Mustermann', age=13)
   print iq

.. testoutput:: pq_based

  >>> InfoQuantity <<<
  array([ 1. ,  2.5,  3. ]) * ms

  Info-Attributes:
   age: 13
   author: 'Mustermann'

**Note**: argument-keywords beat info-keywords. In the following example
13 *and* 16 are assigned to ``age``, but 16 wins:

.. testcode:: pq_based

  iq = InfoQuantity([1,2.5,3], 'ms',
    info={'author': 'Mustermann', 'age':13},
    age = 16)
  print iq

.. testoutput:: pq_based

  >>> InfoQuantity <<<
  array([ 1. ,  2.5,  3. ]) * ms

  Info-Attributes:
   age: 16
   author: 'Mustermann'
