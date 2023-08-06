Tutorial 1 - Using a Simple Serialised Object
=============================================

The simplest use of anamnesis allows the serialisation of classes to and from hdf5
with relatively little extra code.

In order to both reading to and writing from HDF5 files to work, there are
four basic steps

 1. Inherit from the `anamnesis.AbstractAnam` class and call the class constructor
 2. Ensure that your class constructor (`__init__`) can be called with no arguments (you may
    pass arguments to it but they must have default values)
 3. Call the `anamnesis.register_class` function with the class
 4. Populate the `hdf5_outputs` class variable with a list of member variable names necessary for serialisation/de-serialisation

Note that anamnesis uses the fully qualified class name when autoloading during
the unserialising (loading) of object. If you want to use locally defined
classes, you will have to ensure that they have been manually imported.  For
our examples, we will place our classes in the files `test_classesX.py` (where
X is an ineger) and ensure that we can import this file into Python (i.e. it is
on the `PYTHONPATH` or in the current working directory).

Our first example class is going to be a simple model of a person's name
and age.  We place the following code in `test_classes1.py`

.. literalinclude:: test_classes1.py
    :language: python

If we examine the `person` group in the HDF5 file, we can see that the
class member variables:

.. image:: test_classes1.png

We can now write a script which will serial our data into an HDF5 file.
We specify the group name when writing out.

.. literalinclude:: test_script1_write.py
    :language: python

And write another script which loads the class back in.  Because this
class is not registered, we need to make sure that we have imported
the module first.  First of all, we can load from the file; if
we know there is only one group in the file, we do not even need
to specify the group name:

.. literalinclude:: test_script1_read_A.py
    :language: python

If we want to load multiple objects from the same HDF5 file, we can
open the file once and then use a function which loads from
the group of the opened file.  We can also tell anamnesis that
it should autoload modules which start with a certain name.
Both of these possibilities are demonstrated in the script
`test_script1_read_B.py`:

.. literalinclude:: test_script1_read_B.py
    :language: python

