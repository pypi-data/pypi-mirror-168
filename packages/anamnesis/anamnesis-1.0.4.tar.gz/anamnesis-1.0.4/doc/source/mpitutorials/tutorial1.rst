Tutorial 1 - Broadcasting classes using MPI
===========================================

As well as serialisation to and from HDF5, Anamnesis provides wrapper functionality
to allow information to be sent between MPI nodes.

The use of the MPI functions in anamnesis requires the availability of the
`mpi4py` module.  If this is not available, you will not be able to use
the MPI functions fully.  You can, however, set `use_mpi=True` when creating
the `MPIHandler()` object (see below) and then continue to use the functions.
This allows you to write a single code base which will work both when doing
multi-processing using MPI and running on a single machine.

The MPI functions require the same setup (primarily the `hdf5_outputs` class variable)
as are used for the HDF5 serialisation / unserialisation, so we suggest that you
work through the Serialisation tutorials first.

We are going to re-use some of the classes from the previous example.
We place this code in `test_mpiclasses.py`

.. literalinclude:: test_mpiclasses.py
    :language: python

We now write a simple Python script which uses the Anamnesis MPI interface.  We
will design this code so that the master node creates an instance of two of the
classes and the slave nodes receive copies of these.

.. literalinclude:: test_script1.py
    :language: python

To run this code, we need to execute it in an MPI environment.  As usual, make
sure that anamnesis is on the `PYTHONPATH`.

We can then call `mpirun` directly:

.. code-block:: console

    $ mpirun -np 2 python3 test_script1.py

    Master node
    Master: Person: Fred 42
    Master: Place 1: York
    Slave node 1
    Master: Place 2: Glasgow
    Slave node 1: Person: Fred 42
    Slave node 1: Place 1: York
    Slave node 1: Place 2: Glasgow


If you are using a cluster of some form (for instance `gridengine`), you
will need to make sure that you have a queue with MPI enabled and that
you submit your job to that queue.  `Gridengine` in particular has
good tight MPI integration which will transparently handle setting
up the necessary hostlists.

The first thing which we need to do in the script is to initalise our
`MPIHandler`.  This is a singleton object and the `use_mpi` argument
is only examined on the first use.  This means that in future calls,
you can call it without passing any argument.

.. code-block:: python

    m = MPIHandler(use_mpi=True)


In MPI, each instance of the script gets given a node number.  By convention,
we consider node 0 as the master node.  All other nodes are designated as
slave nodes.  In order to decide whether we are the master node, we can
therefore check whether our `rank` (stored on our `MPIHandler` object) is
0.

If we are the master, we then create three objects (a Person, a Place
and a Train), set their attributes and print them out for reference.
We then broadcast each of them in turn to our slave node or nodes.

On the slave node(s), we simply wait to receive the objects which are
being sent from the master.  There are two things to note.  First, we
do not need to specify the object type on the slave, this information
is included in the MPI transfer.  Second, we *must* make sure that
our transmit and receive code is lined up; i.e. if we broadcast three
items, every slave must receive three items.  Code errors of this form
are one of the most common MPI debugging problems.  Try and keep your
transmit / receive logic tidy and well understood in order to avoid
long debugging sessions [#f1].

Once we have recieved the objects, we can simply use them as we normally
would.  Note that the objects are *not* shared before the two processes,
you now have two distinct copies of each object.

Finally, it is important to call the `MPIHandler.done()` method to
indicate to the MPI library that you have successfully finished.

.. rubric:: Fotenotes

.. [#f1] Note that mpi4py under Python3 has an unfortunate tendency to
         swallow error messages which can make debugging frustrating.
         This seems to have got worse since the python2 version.
         Any suggestions as to how to improve this situation would be
         gratefully recieved by the anamnesis authors.
