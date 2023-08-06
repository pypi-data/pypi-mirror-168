# vim: set noexpandtab ts=4 sw=4:

all:
	python3 setup.py build

doc: doc-html

doc-html: all
	python3 setup.py build_sphinx

clean:
	python3 setup.py clean
	# Stupid python setuptools don't even clean the build directory
	rm -fr build
	rm -fr doc/build

flake8:
	flake8 anamnesis

black:
	black anamnesis

isort:
	isort anamnesis

test: all
	py.test-3 -c setup.cfg anamnesis

testv: all
	py.test-3 -c setup.cfg -v anamnesis

install:
	python3 setup.py install --prefix=$(DESTDIR)/usr
	mkdir -p $(DESTDIR)/usr/share/doc/anam
	cp -a doc/build/html $(DESTDIR)/usr/share/doc/anam

.PHONY: clean doc doc-html all test testv flake8 black isort
