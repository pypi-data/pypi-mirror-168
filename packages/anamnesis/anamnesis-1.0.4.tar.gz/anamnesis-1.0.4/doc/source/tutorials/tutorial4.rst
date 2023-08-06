Tutorial 4 - The `Store` class - saving data quickly
====================================================

The `anamnesis.Store` class can be used as a very simple way of storing data
without having to define your own class.

To use the `Store` class, you simply have to place any data which you
want to serialise into the `extra_data` member variable.

As usual with the tutorials, we start with a script which creates an example
test file: `test_script4_write.py`:

.. literalinclude:: test_script4_write.py
    :language: python


Reading back a Store
--------------------

Reading back a `Store` is no different to reading any other anamnesis object
as can be seen in `test_script4_read.py`.

.. literalinclude:: test_script4_read.py
    :language: python

