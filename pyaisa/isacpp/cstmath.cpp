//
// Copyright (c) Pyaisa 2015  - Alberto Lorenzo (alorenzo.md@gmail.com)
//
// Distributed under the MIT License.
// (See accompanying file "copying" or copy at
// http://opensource.org/licenses/MIT)
//

#include <cmath>

#include "cstmath.h"

namespace custom_math {

    double sgn(const double &x) {

        return (x > 0.) - (x < 0.);
    }

    double d(const double &x) {

        if(std::abs(x) < 1e-12)
            return 1.;
        else
            return 0.;
    }

    double u(const double &x) {

        return (1. + sgn(x)) / 2. + d(x) / 2.;
    }

}
