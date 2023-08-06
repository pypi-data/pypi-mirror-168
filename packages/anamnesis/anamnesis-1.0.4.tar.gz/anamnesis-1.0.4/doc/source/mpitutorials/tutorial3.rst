Tutorial 3 - Scattering and Gathering data
==========================================

Scattering and gathering numpy arrays
-------------------------------------

As well as broadcasting and transferring objects, we may wish to split data up
for analysis.  This is done using the `scatter_array` and `gather` functions.

In this script, we look at two ways of scattering data and then how to
gather the data back up for consolidation:

.. literalinclude:: test_script3a.py
    :language: python

Scattering Method 1: scatter_array
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The simplest way to scatter data is to use the `scatter_array` function.  This
function always operates on the first dimension.  I.e., if you have three nodes
and a dataset of size `(100, 15, 23)`, the first node will receive data of size
`(34, 15, 23)` and the remaining two nodes `(33, 15, 23)`.

The code will automatically split the array unequally if necessary.

Scattering Method 2: indices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is sometimes more useful to broadcast an entire dataset to all nodes using
`bcast` and then have the nodes split the data up themselves (for instance, if
they need all of the data for part of the computation but should only work
on some of the data for the full computation).

To do this, we can use the `get_scatter_indices` function.  This must be called
with the size of the data which we are "scattering".  In the example in the text
above, we would call this function with the argument `100`.  The function then
returns a list containing a set of arguments to pass to the `range` function.
In the example above, this would be:

.. code-block:: python

    [(0, 34), (34, 67), (67, 100)]

There is an entry in the list for each MPI node.  We broadcast this list to
all MPI nodes which are then responsible for extracting just the part of the
data required, for example (assuming that `m` is our `MPIHandler`):

.. code-block:: python

    all_indices = m.bcast(None)

    my_indices = range(*all_indices[m.rank])


Note that these indices are congruent with the indices used during gather,
so you can safely gather data which has been manually collated in this way.


Gathering numpy arrays
^^^^^^^^^^^^^^^^^^^^^^

Gathering arrays is straightforward.  Use the `gather` function, passing the
partial array from each node.  There is an example of this in
`test_script3a.py` above.  (Note that by default, the data is gathered to the
root node).


Scattering and gathering lists
------------------------------

Scattering and gathering lists is similar to the process for arrays.  There are
two differences.  The first is that you need to use the `scatter_list` and
`gather_list` routines.  The second is that the `gather_list` routine needs
to be told the total length of the combined list, and on nodes where you
want to receive the full list (including the master), you must pass
`return_all` as `True` (the default is `False`).

An example script can be seen below:

.. literalinclude:: test_script3b.py
    :language: python
