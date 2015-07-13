source activate _test
pip install pytest-cov coveralls
export CDIR=$(pwd)
export SP=$(python -c "import site;print(site.getsitepackages()[0])")
cp .coveragerc $SP/pyaisa/
cd $SP
py.test --cov pyaisa pyaisa/test --cov-config pyaisa/.coveragerc
cp .coverage $CDIR/
cd $CDIR
coveralls
