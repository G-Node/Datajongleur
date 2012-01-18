=================
Data Access Layer
=================

SQLAlchemy
==========

Mapping specific types like ``uuid`` and ``arrays``:

.. todo::

   Specific types have to be adjusted for PostgreSQL

.. todo::

   Addendum mapping doesn't work


Relationships between "Relatives" (Joined Table Inheritance)
------------------------------------------------------------

SQLAlchemy needs explicit information about Foreign Keys. For discussion of
that issue on `Stackoverflow <stackoverflow.com>`_ see:

* `<http://stackoverflow.com/questions/4001215/sqlalchemy-multiple-relationships-many-to-many-via-association-object>`_
* `<http://stackoverflow.com/questions/4864935/sqlalchemy-inheritance-and-relationships>`_
