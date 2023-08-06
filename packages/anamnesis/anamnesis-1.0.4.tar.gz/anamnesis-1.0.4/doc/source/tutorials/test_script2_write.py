#!/usr/bin/python3

import shutil

import h5py

from test_classes2 import (ComplexPerson,
                           ComplexPlace,
                           ComplexTrain)

# Create a person and a place
s = ComplexPerson('Anna', 45)

print(s.name)
print(s.age)

loc = ComplexPlace('York')
print(loc.location)

t = ComplexTrain('Glasgow')
print(t.destination)

# Serialise the person and place to disk
f = h5py.File('test_script2.hdf5', 'w')
s.to_hdf5(f.create_group(s.hdf5_defaultgroup))
loc.to_hdf5(f.create_group(loc.hdf5_defaultgroup))
t.to_hdf5(f.create_group(t.hdf5_defaultgroup))
f.close()

# Serialise the person to disk using a different name
# To do this, we copy the HDF5 file and manually edit it
shutil.copyfile('test_script2.hdf5', 'test_script2_aliases.hdf5')
f = h5py.File('test_script2_alias.hdf5', 'a')
f['person'].attrs['class'] = 'test_classes2.OldComplexPerson'
f.close()
