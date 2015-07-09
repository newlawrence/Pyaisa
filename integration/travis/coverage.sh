source activate _test
pip install pytest-cov
export CDIR=$(pwd)
export SP=$(python -c "import site;print(site.getsitepackages()[0])")
cp .coveragerc $SP/pysapp/
cd $SP
py.test --cov pysapp pysapp/test --cov-config pysapp/.coveragerc
cp .coverage $CDIR/
