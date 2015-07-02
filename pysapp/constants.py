'''
Copyright (c) Pysapp 2015  - Alberto Lorenzo (alorenzo.md@gmail.com)

Distributed under the MIT License.
(See accompanying file "copying" or copy at
http://opensource.org/licenses/MIT)
'''

import numpy as np

INTS = {'psize': -1}
DOUBLES = {'R': 287.05287,
           'g': 9.80665,
           'T0': 288.15,
           'p0': 101325.}
ARRAYS = {'h': np.array([0., 11000., 20000., 32000.]),
          'a': np.array([-0.0065, 0.0000, 0.0010])}


class isa_params(dict):

    def __init__(self, **kwargs):

        super().__init__()
        super().update(INTS)
        super().update(DOUBLES)
        super().__setitem__('layers', ARRAYS)

        if 'callback' in kwargs.keys():
            self.callback = kwargs['callback']
        else:
            self.callback = None

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __getitem__(self, key):

        return super().__getitem__(key)

    def __setitem__(self, key, value):

        if key in INTS.keys():
            super().__setitem__(key, int(value))
        elif key in DOUBLES.keys():
            super().__setitem__(key, float(value))
        elif key == 'layers':
            layers = {'h': np.atleast_1d(value['h']).astype(float),
                      'a': np.atleast_1d(value['a']).astype(float)}
            nh, na = layers['h'].size, layers['a'].size
            assert nh == na + 1 and na > 0, \
                '"h" array must be a unit higher than "a" array in size'
            super().__setitem__(key, layers)

        if self.callback is not None:
            self.callback()

    def __delitem__(self, key):
        pass
