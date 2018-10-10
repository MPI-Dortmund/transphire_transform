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
import pytest
from .. import mrc

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_TEST_FOLDER = 'OUTPUT_TESTS_DUMP'
INPUT_TEST_FOLDER = '../../../test_files'


class TestLoadMrcHeader:

    def test_header_contains_phase_plate(self):
        """
        """
        header = mrc.load_mrc_header(os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'mrc_test.mrc'))
        assert 'Phase Plate' in header

    def test_phase_plate_is_false(self):
        """
        """
        header = mrc.load_mrc_header(os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'mrc_test.mrc'))
        assert not header['Phase Plate']

    def test_phase_plate_is_true(self):
        """
        """
        header = mrc.load_mrc_header(os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'mrc_vpp_test.mrc'))
        assert header['Phase Plate']

    def test_file_does_not_exists_raises_IOError(self):
        """
        """
        with pytest.raises(IOError):
            header = mrc.load_mrc_header(os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'dummy'))