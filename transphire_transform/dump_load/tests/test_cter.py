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

from .. import cter

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


class TestGetCterV10HeaderNames:

    def test_call_functions_should_return_filled_list(self):
        data = [
            'defocus',
            'cs',
            'kv',
            'pixel_size',
            'b_factor',
            'total_ac',
            'astigmatism_amplitude',
            'astigmatism_angle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit',
            'nyquist',
            'spare_1',
            'spare_2',
            'ac',
            'phase_shift',
            'micrograph_name'
            ]
        assert cter.get_cter_v1_0_header_names() == data


class TestLoadCterV10:

    def test_correct_file_should_return_filled_data_frame(self):
        file_name = os.path.join(THIS_DIR, 'cter_v1_0.txt')
        return_frame = cter.load_cter_v1_0(file_name=file_name)

        columns = (
            'defocus_u',
            'defocus_v',
            'cs',
            'kv',
            'pixel_size',
            'b_factor',
            'total_ac',
            'astigmatism_angle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit',
            'nyquist',
            'spare_1',
            'spare_2',
            'ac',
            'phase_shift',
            'micrograph_name'
            )
        data = [
            22862.365,
            22257.635,
            0.01,
            300,
            1.14,
            0,
            0.1,
            19.435,
            0.0010212,
            0,
            0.0021005,
            6.5849,
            0.045268,
            3.4734,
            0.43346,
            0.35979,
            0.4386,
            0.4386,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )

        assert data_frame.equals(return_frame.round(7))


class TestDefocusDefocusDiffToDefocuUAndV:

    def test_defocus_2_um_zero_astigmatism_should_return_20000_angstrom(self):
        def_u, _ = cter.defocus_defocus_diff_to_defocus_u_and_v(2, 0)
        assert def_u == 20000

    def test_zero_astigmatism_should_return_same_values(self):
        def_u, def_v = cter.defocus_defocus_diff_to_defocus_u_and_v(2, 0)
        assert def_u == def_v

    def test_values_should_return_correct_defocus_u(self):
        def_u, _ = cter.defocus_defocus_diff_to_defocus_u_and_v(2.05, 0.1)
        assert def_u == 21000

    def test_values_should_return_correct_defocus_v(self):
        _, def_v = cter.defocus_defocus_diff_to_defocus_u_and_v(2.05, 0.1)
        assert def_v == 20000

    def test_multi_input_should_return_multi_output_defocus_u(self):
        def_u, _ = cter.defocus_defocus_diff_to_defocus_u_and_v(
            pd.Series([2, 2.05]),
            pd.Series([0, 0.1])
            )
        assert def_u.equals(pd.Series([20000, 21000], dtype=float))

    def test_multi_input_should_return_multi_output_defocus_v(self):
        _, def_v = cter.defocus_defocus_diff_to_defocus_u_and_v(
            pd.Series([2, 2.05]),
            pd.Series([0, 0.1])
            )
        assert def_v.equals(pd.Series([20000, 20000], dtype=float))


class TestDefocuUAndVToDefocusDefocusDiff:

    def test_defocus_u_2_um_defocus_v_2_um_should_return_20000_angstrom(self):
        defocus, _ = cter.defocus_u_and_v_to_defocus_defocus_diff(20000, 20000)
        assert defocus == 2

    def test_zero_astigmatism_should_return_same_values(self):
        _, astigmatism = cter.defocus_u_and_v_to_defocus_defocus_diff(20000, 20000)
        assert astigmatism == 0

    def test_values_should_return_correct_defocus_u(self):
        defocus, astigmatism = cter.defocus_u_and_v_to_defocus_defocus_diff(21000, 20000)
        assert defocus == 2.05

    def test_values_should_return_correct_defocus_v(self):
        defocus, astigmatism = cter.defocus_u_and_v_to_defocus_defocus_diff(21000, 20000)
        assert astigmatism == 0.1

    def test_multi_input_should_return_multi_output_defocus(self):
        defocus, _ = cter.defocus_u_and_v_to_defocus_defocus_diff(
            pd.Series([20000, 21000]),
            pd.Series([20000, 20000])
            )
        assert defocus.equals(pd.Series([2, 2.05], dtype=float))

    def test_multi_input_should_return_multi_output_astigmatism(self):
        _, astigmatism = cter.defocus_u_and_v_to_defocus_defocus_diff(
            pd.Series([20000, 21000]),
            pd.Series([20000, 20000])
            )
        assert astigmatism.equals(pd.Series([0, 0.1], dtype=float))
