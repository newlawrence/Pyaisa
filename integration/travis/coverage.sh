source activate _test
pip install pytest-cov
pip install python-coverage
export SP=$(python -c "import site;print(site.getsitepackages()[0])")
cp .coveragerc $SP/pysapp/
py.test --cov $SP/pysapp $SP/pysapp/test --cov-config $SP/pysapp/.coveragerc
cp $SP/pysapp/.coverage ./
