Tutorial 2 - Sending to/from different nodes
============================================

In many cases, we will not want to send data just from the master
node to all other nodes.  We can use a combination of `bcast`, `send`
and `recv` to flexibly send around objects.

Again, for this example we are going to re-use some of the classes from the
previous example which must be in `test_mpiclasses.py` (see Tutorial 1
for details).

Our new script looks like this:

.. literalinclude:: test_script2.py
    :language: python


Again, we need to run this code under an MPI environment (refer back to
Tutorial 1 for details).  We will get the following output:

.. code-block:: console

    Master node
    Master: Created Person: Fred 42
    Slave node 1
    Slave node 2
    Slave node 1: Recieved Person: Fred 42
    Slave node 1: Created place: Manchester
    Slave node 2: Received Person: Fred 42
    Slave node 2: Received Place: Manchester
    Master: Recieved Place: Manchester
    Slave node 2: Created train: Durham
    ComplexTrain.init_from_hdf5
    We have already set destination: Durham
    Slave node 1: Received Train: Fred 42


In order, our script does the following:

1. Set up MPI
2. Create a Person on node 0 (master) and `bcast` it to nodes 1 and 2
3. Create a Place on node 1 and `bcast` it to nodes 0 and 1
4. Create a Train on node 2 and `send` it to node 1 only (on which we call `recv`)

Using these examples, you should be able to see how we can flexibly send
objects around our system.
