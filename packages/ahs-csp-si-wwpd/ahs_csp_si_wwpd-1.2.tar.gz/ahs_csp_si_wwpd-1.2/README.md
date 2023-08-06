This is a private repo for creating the wwpd each week.

It is built doing the following:
- create the virtual env:
- install build
- install twine
- check the version -- any new deployment requires new version number
- build it
- push to pypi


You will need to have your pypi credentials set locally:
https://pypi.org/help/#apitoken
`
python3 -m venv venv
source venv/bin/activate
# check version in setup.py
python3 -m pip install build
python3 -m pip install twine
python3 -m build
python3 -m twine upload dist/package_name
`