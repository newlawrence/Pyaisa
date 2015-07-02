'''
Copyright (c) Pysapp 2015  - Alberto Lorenzo (alorenzo.md@gmail.com)

Distributed under the MIT License.
(See accompanying file "copying" or copy at
http://opensource.org/licenses/MIT)
'''

from warnings import warn

import numpy as np

from pysapp.isacpp import ISACpp
from pysapp.constants import isa_params
from pysapp.performance import get_opt_parallel


class ISA:

    __default_parallel = get_opt_parallel()

    def __init__(self, **kwargs):

        self.__update_changes = False

        if 'psize' in kwargs.keys():
            self.__params = isa_params(callback=self.__refresh, **kwargs)
        else:
            self.__params = isa_params(psize=ISA._ISA__default_parallel,
                                       callback=self.__refresh, **kwargs)

        self.__update_changes = True
        self.__refresh()

    def __refresh(self):

        if self.__update_changes:
            self.__ISA = ISACpp(self.__params['R'], self.__params['g'],
                                self.__params['layers']['h'],
                                self.__params['layers']['a'],
                                self.__params['T0'], self.__params['p0'],
                                self.__params['psize'])

    @property
    def params(self):

        return self.__params

    def atm(self, h):

        h = np.atleast_1d(h).astype(float)
        T = np.empty(h.shape)
        p = np.empty(h.shape)
        rho = np.empty(h.shape)

        error = self.__ISA.atm(h, T, p, rho)
        if(error > 0):
            warn('Altitude value outside range', RuntimeWarning)

        if h.shape[0] == 1:
            return T.item(), p.item(), rho.item()
        else:
            return T, p, rho


def build_atm(**kwargs):

    default_isa = ISA(**kwargs)

    def atm(h, dT=0.):

        if dT != 0.:
            params = default_isa.params.copy()
            params['T0'] += dT
            isa = ISA(**params)
            return isa.atm(h)
        else:
            return default_isa.atm(h)
    return atm

atm = build_atm()
