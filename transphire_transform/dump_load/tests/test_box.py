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
import pandas as pd

from .. import box

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_TEST_FOLDER = '../../../test_files'


class TestLoadEman1:

    def test_box_file_should_import_correct_values(self):
        input_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'box_eman1.box')
        box_coords = [
            [ 995+352//2,   11+352//2],
            [ 918+352//2, 3098+352//2],
            [2220+352//2, 2053+352//2],
            [2959+352//2, 1643+352//2],
            [3446+352//2,  922+352//2],
            [3459+352//2, 2076+352//2],
            [3231+352//2, 1717+352//2],
            [2614+352//2, 2845+352//2],
            [ 668+352//2,  749+352//2],
            [3129+352//2,  954+352//2],
            ]
        data_frame = pd.DataFrame(box_coords, columns=['CoordinateX', 'CoordinateY'])
        return_frame = box.load_eman1(input_file)
        assert data_frame.equals(return_frame)


class TestLoadBox:

    def test_box_file_should_import_correct_values(self):
        input_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'box_eman1.box')
        box_coords = [
            [ 995+352//2,   11+352//2],
            [ 918+352//2, 3098+352//2],
            [2220+352//2, 2053+352//2],
            [2959+352//2, 1643+352//2],
            [3446+352//2,  922+352//2],
            [3459+352//2, 2076+352//2],
            [3231+352//2, 1717+352//2],
            [2614+352//2, 2845+352//2],
            [ 668+352//2,  749+352//2],
            [3129+352//2,  954+352//2],
            ]
        data_frame = pd.DataFrame(box_coords, columns=['CoordinateX', 'CoordinateY'])
        return_frame = box.load_box(input_file, 'eman1')
        assert data_frame.equals(return_frame)

    def test_unknown_key_should_raise_KeyError(self):
        input_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'box_eman1.box')
        with pytest.raises(KeyError):
            return_frame = box.load_box(input_file, 'dummy')
