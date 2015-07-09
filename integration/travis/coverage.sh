pip install pytest-cov
conda install pysapp --use-local --quiet
export SP=$(python -c "import site; print(site.getsitepackages()[0])")
cp .coveragerc $SP/pysapp/
cd $SP
py.test --cov pysapp pysapp/test
