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

import os

import numpy as np
import pandas as pd
import pytest

from .. import ctffind

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture('module')
def ctffind4_data():
    return os.path.join(THIS_DIR, 'ctffind.txt'), 1.090, 300.0, 0.01, 0.07, 'test_file.mrc', '4.1.10'

class TestGetCtffind4HeaderNames:

    def test_call_functions_returns_list(self):
        values = [
            'defocus_u',
            'defocus_v',
            'astigmatism_angle',
            'phase_shift',
            'cross_correlation',
            'resolution_limit',
            ]
        assert ctffind.get_ctffind4_header_names() == values


class TestGetCtffind4Meta:

    def test_correct_file_should_return_filled_data_frame(self, ctffind4_data):
        ctffind4_file, apix, kv, cs, ac, file_name, version = ctffind4_data
        data_frame = pd.DataFrame(
            [[version, file_name, apix, kv, cs, ac]],
            columns=('version', 'micrograph_name', 'pixel_size', 'kv', 'cs', 'ac')
            )
        return_frame = ctffind.get_ctffind4_meta(ctffind4_file)
        assert data_frame.equals(return_frame)

    def test_corrupt_file_should_raise_assertionerror(self):
        with pytest.raises(AssertionError):
            return_frame = ctffind.get_ctffind4_meta(os.path.join(THIS_DIR, 'ctffind_corrupt.txt'))

