# anamnesis

This repository contains the anamnesis python module.  This is a python module
which enables easy serialisation of python objects to/from HDF5 files as well
as between machines using the Message Passing Interface (MPI) via mpi4py.

anamnesis was originally part of the Neuroimaging Analysis Framework (NAF)
which is available from <https://vcs.ynic.york.ac.uk/naf>.  It was split out as a
separate module in order to allow for its use in other modules (such as the
replacement for NAF, YNE: <https://github.com/sails-dev/yne>.


# Authors

 * Mark Hymers <mark.hymers@hankel.co.uk>


# License

This project is currently licensed under the GNU General Public Licence 2.0
or higher.  For alternative license arrangements, please contact the authors.


# Dependencies

See the `requirements.txt` file.

Some of these aren't strict dependencies, but are instead what we develop
against (i.e. we don't guarantee not to use features which only exist from that
release onwards).
