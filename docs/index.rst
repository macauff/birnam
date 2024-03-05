.. birnam documentation master file, created by
   sphinx-quickstart on Tue Jun 23 14:13:11 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#######
birnam
#######
**The Python package for Bringing Independent Results together to Notify of Associations across Multiple catalogues**

``birnam`` is a package for combining individual two-catalogue cross-matches into a "super-match." Starting from a primary dataset, adding matches to a number of secondary catalogues, it reports on the total band-merged object, giving magnitudes across many different wavelengths for each primary-catalogue source. As it builds on `macauff <https://macauff.readthedocs.io/en/latest/>`_, the spectral energy distributions produced are probabilistic, and can be filtered for quality cuts and individually-low chance objects removed from ensemble primary-dataset objects.

.. _getting-started:

************
Installation
************

The instructions for installing ``birnam`` can be found :doc:`here<installation>`.

.. _quick-start:

***********
Quick Start
***********

A quick-start guide is available :doc:`here<quickstart>`.

******************
User Documentation
******************

.. toctree::
   :maxdepth: 1

   birnam

******
Search
******

* :ref:`search`

.. toctree::
   :hidden:

   installation
   quickstart

