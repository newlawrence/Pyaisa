conda install pytest
pip install pytest-cov
python setup.py build_ext --inplace
pip install -e .
py.test --cov pysapp
