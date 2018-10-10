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

from .. import unblur

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_TEST_FOLDER = '../../../test_files'


class TestLoadUnblur102:

    def test_file_reads_correct_data(self):
        input_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'unblur_v1_0_2.txt')
        data = [
            [ 0.137192,  0.199883],
            [-0.040513, -0.095017],
            [-0.219671, -0.290875],
            [-0.205470, -0.403421],
            [-0.316392, -0.403619],
            [-0.173026, -0.324447],
            [-0.213839, -0.267663],
            [-0.232074, -0.254690],
            [-0.054080, -0.218431],
            [-0.121877, -0.156331],
            [-0.057474, -0.109301],
            [-0.042144, -0.067469],
            [ 0.000000,  0.000000],
            [ 0.088806,  0.100347],
            [ 0.158323,  0.180104],
            [ 0.361292,  0.203912],
            [ 0.327297,  0.240433],
            [ 0.334466,  0.308663],
            [ 0.409302,  0.342468],
            [ 0.382510,  0.348759],
            [ 0.468871,  0.345967],
            [ 0.428721,  0.350981],
            [ 0.458751,  0.358079],
            [ 0.500270,  0.370372],
            ]
        data_frame = pd.DataFrame(data, columns=['shift_x', 'shift_y'])
        data_frame['shift_x'] -= data_frame['shift_x'].iloc[0]
        data_frame['shift_y'] -= data_frame['shift_y'].iloc[0]
        return_frame = unblur.load_unblur_1_0_2(input_file)
        assert data_frame.round(4).equals(return_frame.round(4))


class TestLoadUnblur:

    def test_file_version_1_0_2_reads_correct_data(self):
        input_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'unblur_v1_0_2.txt')
        data = [
            [ 0.137192,  0.199883],
            [-0.040513, -0.095017],
            [-0.219671, -0.290875],
            [-0.205470, -0.403421],
            [-0.316392, -0.403619],
            [-0.173026, -0.324447],
            [-0.213839, -0.267663],
            [-0.232074, -0.254690],
            [-0.054080, -0.218431],
            [-0.121877, -0.156331],
            [-0.057474, -0.109301],
            [-0.042144, -0.067469],
            [ 0.000000,  0.000000],
            [ 0.088806,  0.100347],
            [ 0.158323,  0.180104],
            [ 0.361292,  0.203912],
            [ 0.327297,  0.240433],
            [ 0.334466,  0.308663],
            [ 0.409302,  0.342468],
            [ 0.382510,  0.348759],
            [ 0.468871,  0.345967],
            [ 0.428721,  0.350981],
            [ 0.458751,  0.358079],
            [ 0.500270,  0.370372],
            ]
        data_frame = pd.DataFrame(data, columns=['shift_x', 'shift_y'])
        data_frame['shift_x'] -= data_frame['shift_x'].iloc[0]
        data_frame['shift_y'] -= data_frame['shift_y'].iloc[0]
        return_frame = unblur.load_unblur(input_file, '1.0.2')
        assert data_frame.round(4).equals(return_frame.round(4))
