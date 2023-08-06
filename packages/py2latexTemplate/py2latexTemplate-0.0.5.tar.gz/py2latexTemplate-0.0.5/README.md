```command
python setup.py sdist 
pip install .
# or `pip-sync`
```
If actually want to publish package:
```command
python -m pip install build twine
```