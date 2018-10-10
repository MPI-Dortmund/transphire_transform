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

import pandas as pd

from .. import motioncor2

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_TEST_FOLDER = '../../../test_files'


class TestLoadMotioncor100:

    def test_file_reads_correct_data(self):
        input_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'motioncor2_v1_0_0.txt')
        data = [
            [ 5.59, 13.05],
            [ 3.58, 11.86],
            [ 1.96, 10.55],
            [ 1.68,  9.54],
            [ 0.93,  9.01],
            [ 0.60,  8.12],
            [ 0.21,  7.49],
            [ 0.00,  6.73],
            [-0.36,  6.36],
            [-0.16,  5.96],
            [-0.31,  5.06],
            [-0.08,  4.42],
            [-0.15,  3.76],
            [-0.17,  3.22],
            [-0.11,  3.09],
            [ 0.51,  3.18],
            [ 0.31,  2.62],
            [ 0.47,  2.06],
            [ 0.04,  1.34],
            [ 0.34,  0.86],
            [ 0.00,  0.00],
            [ 0.14, -0.58],
            [-0.02, -1.02],
            [ 0.08, -1.81],
            [-0.32, -2.34],
            [-0.16, -2.89],
            [-0.43, -3.53],
            [-0.10, -4.21],
            [-0.23, -4.68],
            [-0.25, -5.30],
            [-0.01, -6.11],
            [-0.27, -6.45],
            [ 0.27, -7.26],
            [ 0.33, -8.21],
            [ 0.05, -8.61],
            [-0.07, -9.02],
            [-0.48, -9.25],
            [-0.75, -9.76],
            [-0.67,-10.42],
            [-0.73,-10.86],
            ]
        data_frame = pd.DataFrame(data, columns=['shift_x', 'shift_y'])
        data_frame['shift_x'] -= data_frame['shift_x'].iloc[0]
        data_frame['shift_y'] -= data_frame['shift_y'].iloc[0]
        return_frame = motioncor2.load_motioncor2_1_0_0(input_file)
        assert data_frame.equals(return_frame)


class TestLoadMotioncor:

    def test_file_version_1_0_0_reads_correct_data(self):
        input_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'motioncor2_v1_0_0.txt')
        data = [
            [ 5.59, 13.05],
            [ 3.58, 11.86],
            [ 1.96, 10.55],
            [ 1.68,  9.54],
            [ 0.93,  9.01],
            [ 0.60,  8.12],
            [ 0.21,  7.49],
            [ 0.00,  6.73],
            [-0.36,  6.36],
            [-0.16,  5.96],
            [-0.31,  5.06],
            [-0.08,  4.42],
            [-0.15,  3.76],
            [-0.17,  3.22],
            [-0.11,  3.09],
            [ 0.51,  3.18],
            [ 0.31,  2.62],
            [ 0.47,  2.06],
            [ 0.04,  1.34],
            [ 0.34,  0.86],
            [ 0.00,  0.00],
            [ 0.14, -0.58],
            [-0.02, -1.02],
            [ 0.08, -1.81],
            [-0.32, -2.34],
            [-0.16, -2.89],
            [-0.43, -3.53],
            [-0.10, -4.21],
            [-0.23, -4.68],
            [-0.25, -5.30],
            [-0.01, -6.11],
            [-0.27, -6.45],
            [ 0.27, -7.26],
            [ 0.33, -8.21],
            [ 0.05, -8.61],
            [-0.07, -9.02],
            [-0.48, -9.25],
            [-0.75, -9.76],
            [-0.67,-10.42],
            [-0.73,-10.86],
            ]
        data_frame = pd.DataFrame(data, columns=['shift_x', 'shift_y'])
        data_frame['shift_x'] -= data_frame['shift_x'].iloc[0]
        data_frame['shift_y'] -= data_frame['shift_y'].iloc[0]
        return_frame = motioncor2.load_motioncor2(input_file, '1.0.0')
        assert data_frame.equals(return_frame)
