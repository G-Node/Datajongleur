.. index::
   single: troubleshooting
   single: faq; troubleshooting

.. _troubleshooting:

===============
Troubleshooting
===============

.. _InvalidRequestError:

Error: ``InvalidRequestError``
==============================

Most probably there was an error during the attempt to communicate with the
database. In order to continue working with the database you have to set it
back to the last consistent stage::

  session.rollback()

Error: ``UnboundExecutionError``
================================

This error occurs when you try to access a ``beanbag`` before connecting to the
database. One way to connect correctly to the database is to use
``datajongleur.get_session()`` after importing necessary models::

  import datajongleur as dj
  from datajongleur.beanbags.neuro.pq_based import *
  session = dj.get_session()
