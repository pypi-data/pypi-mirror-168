How to release anamnesis
========================

Before
------
 * Check that all MRs which are intended to be in this release have been merged into master
 * Check that master builds cleanly in CI
 * Set the version and release numbers appropriately in `setup.py` in master
 * Check that the documentation builds
```
make doc-html
```
 * Run the test suite and check there are no failures
```
make testv2
make testv3
```
 * Ensure that you have an up-to-date python3-twine available.  You may have to create a
   virtualenv and install it that way.  If you need to test it, test against `https://test.pypi.org`
   rather than the real `https://pypi.org` (see the Packaging Python Documents tutorial at
   https://packaging.python.org/tutorials/packaging-projects/)
 * Ensure that you have a gitlab API token set up for `gitlab.com`


Release
-------
 * Tag the release in gitlab:
```
git tag x.y.z
git push --tags
```
 * Wait for CI to complete and download the artifacts for PyPi
 * Check the artefacts - untar the source tarball and run the tests again
 * Upload the artefacts to twine (from the `dist/` directory containing the unzipped artefacts.
   An example output is below:
```
python3 -m twine upload *

Enter your username: xxx
Enter your password: yyy
Uploading distributions to https://upload.pypi.org/legacy/
```

 * Store the release in gitlab (including links to pypi) [TODO: Write a script for this]
   You will need to update the variables in the curl snippet below:
```
curl --header 'Content-Type: application/json' \
     --header "PRIVATE-TOKEN: GITLAB_ACCESS_TOKEN_HERE" \
     --data '{ "name": "x.y.z", "tag_name": "x.y.z", "description": "Release description here", "assets": { "links": [{ "name": "anamnesis-x.y.z.tar.gz", "url": "https://files.pythonhosted.org/.../anamnesis-x.y.z.tar.gz" }, { "name": "anamnesis-x.y.z-py3-none-any.whl", "url": "https://files.pythonhosted.org/.../anamnesis-x.y.z-py3-none-any.whl"}] } }' \
     --request POST "https://gitlab.com/api/v4/projects/23672858/releases"
```


After Uploading
---------------

 * Test that you can pip install the toolbox in a clean virtualenv:

```
mkdir /tmp/anamnesis-test
cd /tmp/anamnesis/test
virtualenv -p /usr/bin/python3 .
. bin/activate
pip3 install anamnesis
```
