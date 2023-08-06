# common-connection-layer
---
The common client connection layer Library for(Redis, Cosmos, MySQL, PostgreSQL & ClickHouse)
1. It will return connection object of database based on configuration.


## Getting started

To Use the same run pip install connlayer==0.0.4
For connection read example file /connlayer/test_client.py

## To build and upload to pypi
In case if add others database config we will make build & upload to pypi with new version, steps are
1. python3 -m pip install --upgrade build
2. python3 -m build  ## it will create tar.gz package in disst dir with version
3. python3 -m pip install --upgrade twine
4. python3 -m twine upload --repository testpypi dist/*



