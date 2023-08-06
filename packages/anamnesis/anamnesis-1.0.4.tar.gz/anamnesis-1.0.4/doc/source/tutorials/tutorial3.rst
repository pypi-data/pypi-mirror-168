Tutorial 3 - AnamCollections - dealing with many similar objects
================================================================

The `AnamCollection` code is designed to make it easy to deal with
situations where you have many of the same type of class and
want to perform analysis across them.  For instance, in a
sliding-window analysis, you may have a class which implements
model fitting and metric measurement for a given window.  You
can then use an `AnamCollection` to easily collate the
results together.  You can consider `AnamCollection` to be
a list of objects with additional helper functions to assist
with the collation of data and HDF5 serialisation/deserialisation.

In general, you will want to subclass `AnamCollection` to use
it.  An example can be found in `test_classes3.py`:

.. literalinclude:: test_classes3.py
    :language: python

In this case, we have two variables, each of which will be a
numpy array.  The `AnamCollection` class is specifically
designed for use with numpy arrays.

As an example of using this class when writing, you can see
`test_script3_write.py`:

.. literalinclude:: test_script3_write.py
    :language: python

Note that objects can be appended into the collection object
using the normal `.append()` method and then be written
into an HDF5 file as normal.

When using a `AnamCollection` derived object, the simplest
form of use is to treat it as a list which will let you
retrieve the objects stored within it.  This can
be seen in the first few lines of the script below.

In addition, if you request any of the members which
are referred to in the `anam_combine` member variable
on the collection, the class will collate all of the instances
of the identically named variable from the objects in the
list and return an object which has these objects stacked.
In most cases, you will use this with numpy arrays - you
will then end up with a numpy array with an additional
dimension.  I.e., if each object has a numpy array of
dimension `(10, 10)` and you have 3 objects, the combined
array will have size `(10, 10, 3)`.  The objects are
accessed by just accessing it as a member variable; for instance,
if the name `data` was in `anam_combine` and your collection
was named `collection`, you could access the combined data
by accessing `collection.data`.  Note that this member
will only be available once you have called the `update_cache()`
function on the collection - this is for reasons of efficiency.
Therefore, after modifying, adding or deleting members in the list,
you should call `update_cache()`.  There is also a `clear_cache()`
function but it is rarely used.

For a full example, see `test_script3_read.py`:

.. literalinclude:: test_script3_read.py
    :language: python

