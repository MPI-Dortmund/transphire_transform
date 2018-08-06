"""
MIT License

Copyright (c) 2018 Max Planck Institute of Molecular Physiology

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import pytest
from .. import dump_util


def test_create_header_list():
    """
    """
    header = ['a', 'b', 'c', 'd']
    assert dump_util.create_header(names=header, index=False) == header


def test_create_header_index_list():
    """
    """
    header = ['a', 'b', 'c', 'd']
    header_out = ['a #1', 'b #2', 'c #3', 'd #4']
    assert dump_util.create_header(names=header, index=True) == header_out


def test_create_header_array():
    """
    """
    header = np.array(['a', 'b', 'c', 'd'], dtype=str)
    assert dump_util.create_header(names=header, index=False) == header.tolist()


def test_create_header_index_array():
    """
    """
    header = np.array(['a', 'b', 'c', 'd'], dtype=str)
    header_out = ['a #1', 'b #2', 'c #3', 'd #4']
    assert dump_util.create_header(names=header, index=True) == header_out


def test_create_header_array_empty():
    """
    """
    header = np.array([], dtype=str)
    with pytest.raises(IOError):
        dump_util.create_header(names=header, index=True)


def test_create_header_list():
    """
    """
    header = []
    with pytest.raises(IOError):
        dump_util.create_header(names=header, index=True)


def test_create_header_list_vert():
    """
    """
    header = ['a', 'b', 'c', 'd']
    assert dump_util.create_header(names=header, index=False) == header


def test_create_header_index_list():
    """
    """
    header = ['a', 'b', 'c', 'd']
    header_out = ['a #1', 'b #2', 'c #3', 'd #4']
    assert dump_util.create_header(names=header, index=True) == header_out
