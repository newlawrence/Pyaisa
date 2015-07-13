'''
Copyright (c) Pyaisa 2015  - Alberto Lorenzo (alorenzo.md@gmail.com)

Distributed under the MIT License.
(See accompanying file "copying" or copy at
http://opensource.org/licenses/MIT)
'''

from math import log
from timeit import repeat

from pyaisa.constants import isa_params


def get_opt_parallel(loops=200, repeats=20, imax=4):

    p = isa_params()
    setup = 'from numpy import array, empty, linspace\n' \
            'from pyaisa.isacpp import ISACpp\n' \
            'h = linspace(0., 11000., {})\n' \
            'T = empty(h.shape)\n' \
            'p = empty(h.shape)\n' \
            'rho = empty(h.shape)\n' \
            'isa = ISACpp({}, {}, {}, {}, {}, {}, {})'

    def get_atm_time(i, parallel):

        if parallel:
            t = repeat('isa.atm(h, T, p, rho)',
                       setup=setup.format(10 ** i, p['R'], p['g'],
                                          repr(p['layers']['h']),
                                          repr(p['layers']['a']),
                                          p['T0'], p['p0'], 0),
                       number=loops, repeat=repeats)
        else:
            t = repeat('isa.atm(h, T, p, rho)',
                       setup=setup.format(10 ** i, p['R'], p['g'],
                                          repr(p['layers']['h']),
                                          repr(p['layers']['a']),
                                          p['T0'], p['p0'], -1),
                       number=loops, repeat=repeats)
        return 1e6 * min(t) / loops

    for i in range(imax):

        tp0, tp1 = get_atm_time(i, True), get_atm_time(i + 1, True)
        tnp0, tnp1 = get_atm_time(i, False), get_atm_time(i + 1, False)

        psize = 0 if tp0 > tnp0 else -1
        if (tp1 - tnp1) * (tp0 - tnp0) < 0:
            psize = pow(10, i + log(tp0 / tnp0) / log((tp0 * tnp1) /
                                                      (tp1 * tnp0)))
            break

    if psize == -1:
        return psize
    else:
        return int(psize / 10 ** i) * 10 ** i
