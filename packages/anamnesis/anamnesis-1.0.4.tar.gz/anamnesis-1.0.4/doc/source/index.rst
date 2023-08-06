.. anamnesis documentation master file, created by
   sphinx-quickstart on Tue Jun 27 22:33:00 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

anamnesis documentation
=======================

Contents:

.. toctree::
   :maxdepth: 2

   tutorials
   reference


Introduction
------------

`anamnesis` is a python module which provides the ability to easily
serialise/unserialise Python classes to and from the HDF5 file format.
It aims to be trivial to incorporate (normally requiring only a single
extra class variable to be added to your classes) and flexible.

The library also extends the HDF5 serialisation/unserialisation
capabilities to the MPI framework.  This allows objects to be trivially
passed between nodes in an MPI computation.  The library also provides
some wrapper routines to make it simpler to perform scatter and
gather operations on arrays and lists (lists may even contain
objects to be transferred).

`anamnesis` was originally written as part of the `NeuroImaging Analysis
Framework`, a library intended for use in MEG theory work written at
York NeuroImaging Centre, University of York, UK, but it has been split
out in order to make it more generically useful.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

