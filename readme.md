# Pysapp
Version 0.8.2

ISA Model computed in C++

[![Binstar Badge](https://binstar.org/newlawrence/pysapp/badges/build.svg)](https://binstar.org/newlawrence/pysapp/builds)
[![Binstar Badge](https://binstar.org/newlawrence/pysapp/badges/version.svg)](https://binstar.org/newlawrence/pysapp)
[![Binstar Badge](https://binstar.org/newlawrence/pysapp/badges/license.svg)](https://binstar.org/newlawrence/pysapp)
[![Binstar Badge](https://binstar.org/newlawrence/pysapp/badges/installer/conda.svg)](https://conda.binstar.org/newlawrence)

### A simple Standard Atmosphere Model

This project it's only a simple standard atmosphere model that I've made for learning purposes, and to introduce myself to the Open Source world and its tools. Despite that, the ISA model is fully functional, fast, configurable and compliant with the [COESA](http://hdl.handle.net/2060/19770009539) stdandard.

It is written in Python 3 with a C++ OpenMP powered heart using SWIG for interfacing between those two languages. If you are running a multiple core machine, Pysapp will auto-adjust itself in each situation to perform the fastest as posible.

Pysapp is also fully configurable, so feel free to change every single parameter to adapt the model to whatever atmosphere you want (R, g, T0, p0, number of layers...).

Although the model is finished, there're many more things to do yet: writing the documentation, improving inline comments in the code, adding more tests... so keep an eye on future commits!

### Acknowledgements

Thanks to my friend  Juan Luis Cano [@Juanlu001](https://github.com/Juanlu001), he introduced me in this marvellous world of the Open Source. This project its a tribute to him and all the fantastic [@AeroPython](https://github.com/AeroPython) team.