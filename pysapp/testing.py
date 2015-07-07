'''
Copyright (c) Pysapp 2015  - Alberto Lorenzo (alorenzo.md@gmail.com)

Distributed under the MIT License.
(See accompanying file "copying" or copy at
http://opensource.org/licenses/MIT)
'''

import os.path
import pytest


def test_library():
    pytest.main([os.path.dirname(os.path.abspath(__file__)), ])
