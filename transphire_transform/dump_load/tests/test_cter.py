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
OUTPUT_TEST_FOLDER = 'OUTPUT_TESTS_DUMP'
INPUT_TEST_FOLDER = '../../../test_files'


class TestGetCterV10HeaderNames:

    def test_call_functions_should_return_filled_list(self):
        data = [
            'defocus',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'astigmatism_amplitude',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            ]
        assert cter.get_cter_v1_0_header_names() == data


class TestLoadCterV10:

    def test_correct_multiline_file_should_return_filled_data_frame(self):
        file_name = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'cter_v1_0_multiline.txt')
        return_frame = cter.load_cter_v1_0(file_name=file_name)

        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [[
            22257.635,
            22862.365,
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
            2.307018,
            2.779399,
            2.279982,
            2.279982,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]] * 2
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_correct_file_should_return_filled_data_frame(self):
        file_name = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'cter_v1_0.txt')
        return_frame = cter.load_cter_v1_0(file_name=file_name)

        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [
            22257.635,
            22862.365,
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
            2.307018,
            2.779399,
            2.279982,
            2.279982,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_correct_file_low_angle_should_return_filled_data_frame(self):
        file_name = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'cter_v1_0_low_angle.txt')
        return_frame = cter.load_cter_v1_0(file_name=file_name)

        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [
            22257.635,
            22862.365,
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
            2.307018,
            2.779399,
            2.279982,
            2.279982,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_correct_file_high_angle_should_return_filled_data_frame(self):
        file_name = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'cter_v1_0_high_angle.txt')
        return_frame = cter.load_cter_v1_0(file_name=file_name)

        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [
            22257.635,
            22862.365,
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
            2.307018,
            2.779399,
            2.279982,
            2.279982,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))


class TestDefocusDefocusDiffToDefocuUAndV:

    def test_defocus_2_um_zero_astigmatism_should_return_20000_angstrom(self):
        def_u, _ = cter.defocus_defocus_diff_to_defocus_u_and_v(2, 0)
        assert def_u == 20000

    def test_zero_astigmatism_should_return_same_values(self):
        def_u, def_v = cter.defocus_defocus_diff_to_defocus_u_and_v(2, 0)
        assert def_u == def_v

    def test_values_should_return_correct_defocus_u(self):
        def_u, _ = cter.defocus_defocus_diff_to_defocus_u_and_v(2.05, 0.1)
        assert def_u == 20000

    def test_values_should_return_correct_defocus_v(self):
        _, def_v = cter.defocus_defocus_diff_to_defocus_u_and_v(2.05, 0.1)
        assert def_v == 21000

    def test_values_inverse_should_return_correct_defocus_v(self):
        _, def_v = cter.defocus_defocus_diff_to_defocus_u_and_v(2.05, -0.1)
        assert def_v == 20000

    def test_multi_input_should_return_multi_output_defocus_u(self):
        def_u, _ = cter.defocus_defocus_diff_to_defocus_u_and_v(
            pd.Series([2, 2.05, 2.05]),
            pd.Series([0, -0.1, 0.1])
            )
        assert def_u.equals(pd.Series([20000, 21000, 20000], dtype=float))

    def test_multi_input_should_return_multi_output_defocus_v(self):
        _, def_v = cter.defocus_defocus_diff_to_defocus_u_and_v(
            pd.Series([2, 2.05, 2.05]),
            pd.Series([0, 0.1, -0.1]),
            )
        assert def_v.equals(pd.Series([20000, 21000, 20000], dtype=float))


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
        assert astigmatism == -0.1

    def test_values_invert_should_return_correct_defocus_v(self):
        defocus, astigmatism = cter.defocus_u_and_v_to_defocus_defocus_diff(20000, 21000)
        assert astigmatism == 0.1

    def test_multi_input_should_return_multi_output_defocus(self):
        defocus, _ = cter.defocus_u_and_v_to_defocus_defocus_diff(
            pd.Series([20000, 21000]),
            pd.Series([20000, 20000])
            )
        assert defocus.equals(pd.Series([2, 2.05], dtype=float))

    def test_multi_input_should_return_multi_output_astigmatism(self):
        _, astigmatism = cter.defocus_u_and_v_to_defocus_defocus_diff(
            pd.Series([20000, 21000, 20000]),
            pd.Series([20000, 20000, 21000]),
            )
        assert astigmatism.equals(pd.Series([0., -0.1, 0.1], dtype=float))


class TestDumpCterV10:

    def test_valid_cter_data_should_create_partres_file(self, tmpdir):
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_valid_cter_data_should_create_partres_file.star')
        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [
            22257.635,
            22862.365,
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
        cter.dump_cter_v1_0(output_file, data_frame)
        assert os.path.exists(output_file)

    def test_valid_cter_data_large_angle_should_create_correct_file(self, tmpdir):
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_valid_cter_data_large_angle_should_create_correct_file.star')
        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [
            22257.635,
            22862.365,
            0.01,
            300,
            1.14,
            0,
            0.1,
            19.435+720,
            0.0010212,
            0,
            0.0021005,
            6.5849,
            0.045268,
            3.4734,
            2.30702,
            2.77940,
            2.27998,
            2.77940,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )
        cter.dump_cter_v1_0(output_file, data_frame)

        expected_data = [[
            2.256,
            0.01,
            300.0,
            1.14,
            0.0,
            10.0,
            0.060473,
            25.565 ,
            0.0010212,
            0.0,
            0.0021005,
            6.5849,
            0.045268,
            3.4734,
            0.4334596,
            0.3597899,
            0.4386003,
            0.3597899,
            0.0,
            10.0,
            0.0,
            'test_file.mrc',
            ]]
        input_data = []
        with open(output_file, 'r') as read:
            for idx, line in enumerate(read.readlines()):
                line = line.strip().split()
                input_data.append([])
                for entry in line:
                    try:
                        data = float(entry)
                    except ValueError:
                        data = entry
                    input_data[idx].append(data)

        assert expected_data == input_data

    def test_valid_cter_data_should_create_correct_file(self, tmpdir):
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_valid_cter_data_should_create_correct_partres_file.star')
        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [
            22257.635,
            22862.365,
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
            2.30702,
            2.77940,
            2.27998,
            2.77940,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )
        cter.dump_cter_v1_0(output_file, data_frame)

        expected_data = [[
            2.256,
            0.01,
            300.0,
            1.14,
            0.0,
            10.0,
            0.060473,
            25.565 ,
            0.0010212,
            0.0,
            0.0021005,
            6.5849,
            0.045268,
            3.4734,
            0.4334596,
            0.3597899,
            0.4386003,
            0.3597899,
            0.0,
            10.0,
            0.0,
            'test_file.mrc',
            ]]
        input_data = []
        with open(output_file, 'r') as read:
            for idx, line in enumerate(read.readlines()):
                line = line.strip().split()
                input_data.append([])
                for entry in line:
                    try:
                        data = float(entry)
                    except ValueError:
                        data = entry
                    input_data[idx].append(data)

        assert expected_data == input_data


class TestAmplitudeContrastToAngle:

    def test_zero_should_return_zero(self):
        value = pd.Series([0])
        return_value = pd.Series([0], dtype=float)
        assert cter.amplitude_contrast_to_angle(value).equals(return_value)

    def test_100_should_return_ninety(self):
        value = pd.Series([100])
        return_value = pd.Series([90], dtype=float)
        assert cter.amplitude_contrast_to_angle(value).equals(return_value)

    def test_minus_100_should_return_ninety(self):
        value = pd.Series([-100])
        return_value = pd.Series([90], dtype=float)
        assert cter.amplitude_contrast_to_angle(value).equals(return_value)

    def test_50_should_return_30(self):
        value = pd.Series([50])
        return_value = pd.Series([30], dtype=float)
        data_frame = cter.amplitude_contrast_to_angle(value)
        assert return_value.equals(data_frame.round(1))

    def test_minus_50_should_return_150(self):
        value = pd.Series([-50])
        return_value = pd.Series([150], dtype=float)
        data_frame = cter.amplitude_contrast_to_angle(value)
        assert return_value.equals(data_frame.round(1))

    def test_multiline_should_return_correct_values(self):
        value = pd.Series([0, 100, -100, 50, -50])
        return_value = pd.Series([0, 90, 90, 30, 150], dtype=float)
        data_frame = cter.amplitude_contrast_to_angle(value)
        assert return_value.equals(data_frame.round(1))

    def test_200_should_raise_assertionerror(self):
        value = pd.Series([200])
        with pytest.raises(AssertionError):
            assert cter.amplitude_contrast_to_angle(value)

    def test_minus_200_should_raise_assertionerror(self):
        value = pd.Series([-200])
        with pytest.raises(AssertionError):
            assert cter.amplitude_contrast_to_angle(value)

    def test_muliline_200_should_raise_assertionerror(self):
        value = pd.Series([200, 0, 50])
        with pytest.raises(AssertionError):
            assert cter.amplitude_contrast_to_angle(value)


class TestAngleToAmplitudeContrast:

    def test_zero_should_return_zero(self):
        return_value = pd.Series([0], dtype=float)
        value = pd.Series([0], dtype=float)
        assert cter.angle_to_amplitude_contrast(value).equals(return_value)

    def test_100_should_return_ninety(self):
        return_value = pd.Series([100], dtype=float)
        value = pd.Series([90], dtype=float)
        assert cter.angle_to_amplitude_contrast(value).equals(return_value)

    def test_minus_100_should_return_ninety(self):
        return_value = pd.Series([-100], dtype=float)
        value = pd.Series([-90], dtype=float)
        assert cter.angle_to_amplitude_contrast(value).equals(return_value)

    def test_50_should_return_30(self):
        return_value = pd.Series([50], dtype=float)
        value = pd.Series([30], dtype=float)
        data_frame = cter.angle_to_amplitude_contrast(value)
        assert return_value.equals(data_frame.round(1))

    def test_minus_50_should_return_150(self):
        return_value = pd.Series([-50], dtype=float)
        value = pd.Series([150], dtype=float)
        data_frame = cter.angle_to_amplitude_contrast(value)
        assert return_value.equals(data_frame.round(1))

    def test_multiline_should_return_correct_values(self):
        return_value = pd.Series([0, 100, -100, 50, -50], dtype=float)
        value = pd.Series([0, 90, -90, 30, 150], dtype=float)
        data_frame = cter.angle_to_amplitude_contrast(value)
        assert return_value.equals(data_frame.round(1))


class TestInternToCter:

    def test_input_cter_values_should_return_output_values(self):
        columns = (
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data = [[
            0.1,
            19.435,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            0.1,
            0,
            ]]
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        valid_list = [
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            ]
        cter.intern_to_cter(data_frame, valid_list)

        return_data = [[
            10.0,
            25.565,
            0.4334599903,
            0.3597900122,
            0.4385999539,
            0.3597900122,
            10.0,
            0
            ]]
        return_frame = pd.DataFrame(
            return_data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_input_ctffind_values_should_return_output_values(self):
        columns = (
            'PixelSize',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data = [[
            1.14,
            0,
            19.435,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            0.1,
            0
            ]]
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        valid_list = [
            'DefocusAngle',
            'CtfMaxResolution',
            'nyquist',
            'AmplitudeContrast',
            'PhaseShift',
            ]
        cter.intern_to_cter(data_frame, valid_list)

        return_data = [[
            1.14,
            10.0,
            25.565,
            0.4385999539,
            0.4385999539,
            0.4385999539,
            0.3597900122,
            10.0,
            0
            ]]
        return_frame = pd.DataFrame(
            return_data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_input_ctffind_high_angle_values_should_return_output_values(self):
        columns = (
            'PixelSize',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data = [[
            1.14,
            0,
            19.435+720,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            0.1,
            0
            ]]
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        valid_list = [
            'DefocusAngle',
            'CtfMaxResolution',
            'nyquist',
            'AmplitudeContrast',
            'PhaseShift',
            ]
        cter.intern_to_cter(data_frame, valid_list)

        return_data = [[
            1.14,
            10.0,
            25.565,
            0.4385999539,
            0.4385999539,
            0.4385999539,
            0.3597900122,
            10.0,
            0
            ]]
        return_frame = pd.DataFrame(
            return_data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_input_ctffind_low_angle_values_should_return_output_values(self):
        columns = (
            'PixelSize',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data = [[
            1.14,
            0,
            19.435-720,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            0.1,
            0
            ]]
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        valid_list = [
            'DefocusAngle',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            ]
        cter.intern_to_cter(data_frame, valid_list)

        return_data = [[
            1.14,
            10.0,
            25.565,
            1/(2*1.14),
            1/(2*1.14),
            1/(2*1.14),
            0.3597900122,
            10.0,
            0
            ]]
        return_frame = pd.DataFrame(
            return_data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_input_ctffind_phase_shift_values_should_return_output_values(self):
        columns = (
            'PixelSize',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data = [[
            1.14,
            0,
            19.435-720,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            0.1,
            90
            ]]
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        valid_list = [
            'DefocusAngle',
            'CtfMaxResolution',
            'nyquist',
            'AmplitudeContrast',
            'PhaseShift',
            ]
        cter.intern_to_cter(data_frame, valid_list)

        return_data = [[
            1.14,
            -99.49874,
            25.565,
            0.4385999539,
            0.4385999539,
            0.4385999539,
            0.3597900122,
            10.0,
            90
            ]]
        return_frame = pd.DataFrame(
            return_data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_input_ctffind_phase_shift_multiline_values_should_return_output_values(self):
        columns = (
            'PixelSize',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data = [[
            1.14,
            0,
            19.435-720,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            0.1,
            90
            ]]*2
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        valid_list = [
            'DefocusAngle',
            'CtfMaxResolution',
            'nyquist',
            'AmplitudeContrast',
            'PhaseShift',
            ]
        cter.intern_to_cter(data_frame, valid_list)

        return_data = [[
            1.14,
            -99.49874,
            25.565,
            0.4385999539,
            0.4385999539,
            0.4385999539,
            0.3597900122,
            10.0,
            90
            ]]*2
        return_frame = pd.DataFrame(
            return_data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))


class TestCterToIntern:

    def test_input_cter_should_modify_input_data(self):
        columns_input = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_input = [[
            2,
            0.1,
            -99.49874,
            25.565,
            1/2.307018,
            1/2.779399,
            1/2.279982,
            1/2.779399,
            10,
            90
            ]]
        data_frame = pd.DataFrame(
            data_input,
            columns=columns_input
            )

        columns_output = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_output = [[
            2,
            0.1,
            -0.994987,
            19.435,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            0.1,
            90
            ]]
        return_frame = pd.DataFrame(
            data_output,
            columns=columns_output
            )

        cter.cter_to_intern(data_frame)
        assert return_frame.equals(data_frame.round(6))

    def test_input_cter_should_drop_defocus(self):
        columns_input = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_input = [[
            2,
            0.1,
            -99.49874,
            25.565,
            1/2.307018,
            1/2.779399,
            1/2.279982,
            1/2.779399,
            10,
            90
            ]]
        data_frame = pd.DataFrame(
            data_input,
            columns=columns_input
            )

        _, dropped_data_cter = cter.cter_to_intern(data_frame)
        assert 'defocus' not in dropped_data_cter

    def test_input_cter_should_drop_astigmatism_amplitude(self):
        columns_input = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_input = [[
            2,
            0.1,
            -99.49874,
            25.565,
            1/2.307018,
            1/2.779399,
            1/2.279982,
            1/2.779399,
            10,
            90
            ]]
        data_frame = pd.DataFrame(
            data_input,
            columns=columns_input
            )

        _, dropped_data_cter = cter.cter_to_intern(data_frame)
        assert 'astigmatism_amplitude' not in dropped_data_cter

    def test_input_cter_should_return_correct_defocus_u_and_v(self):
        columns_input = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_input = [[
            2,
            0.2,
            -99.49874,
            25.565,
            1/2.307018,
            1/2.779399,
            1/2.279982,
            1/2.779399,
            10,
            90
            ]]
        data_frame = pd.DataFrame(
            data_input,
            columns=columns_input
            )

        columns_output = (
            'DefocusU',
            'DefocusV'
            )
        data_output = [[
            19000,
            21000,
            ]]
        output_frame = pd.DataFrame(
            data_output,
            columns=columns_output,
            dtype=float
            )

        return_data, _ = cter.cter_to_intern(data_frame)
        assert output_frame.equals(return_data.round(6))

    def test_input_cter_inverse_should_return_correct_defocus_u_and_v(self):
        columns_input = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_input = [[
            2,
            -0.2,
            -99.49874,
            25.565,
            1/2.307018,
            1/2.779399,
            1/2.279982,
            1/2.779399,
            10,
            90
            ]]
        data_frame = pd.DataFrame(
            data_input,
            columns=columns_input
            )

        columns_output = (
            'DefocusU',
            'DefocusV'
            )
        data_output = [[
            21000,
            19000,
            ]]
        output_frame = pd.DataFrame(
            data_output,
            columns=columns_output,
            dtype=float
            )

        return_data, _ = cter.cter_to_intern(data_frame)
        assert output_frame.equals(return_data.round(6))

    def test_input_cter_large_angle_should_modify_input_data(self):
        columns_input = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_input = [[
            2,
            0.1,
            -99.49874,
            25.565+720,
            1/2.307018,
            1/2.779399,
            1/2.279982,
            1/2.779399,
            10,
            90
            ]]
        data_frame = pd.DataFrame(
            data_input,
            columns=columns_input
            )

        columns_output = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_output = [[
            2,
            0.1,
            -0.994987,
            19.435,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            .1,
            90
            ]]
        return_frame = pd.DataFrame(
            data_output,
            columns=columns_output
            )

        cter.cter_to_intern(data_frame)
        assert return_frame.equals(data_frame.round(6))

    def test_input_cter_small_angle_should_modify_input_data(self):
        columns_input = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_input = [[
            2,
            0.1,
            -99.49874,
            25.565-720,
            1/2.307018,
            1/2.779399,
            1/2.279982,
            1/2.779399,
            10,
            90
            ]]
        data_frame = pd.DataFrame(
            data_input,
            columns=columns_input
            )

        columns_output = (
            'defocus',
            'astigmatism_amplitude',
            'total_ac',
            'DefocusAngle',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'AmplitudeContrast',
            'PhaseShift',
            )
        data_output = [[
            2,
            0.1,
            -0.994987,
            19.435,
            2.307018,
            2.779399,
            2.279982,
            2.779399,
            .1,
            90
            ]]
        return_frame = pd.DataFrame(
            data_output,
            columns=columns_output
            )

        cter.cter_to_intern(data_frame)
        assert return_frame.equals(data_frame.round(6))


class TestLoadCter:

    def test_version_1_0_should_return_version_1_0(self):
        file_name = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'cter_v1_0_multiline.txt')
        return_frame = cter.load_cter(file_name=file_name, version='1.0')

        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [[
            22257.635,
            22862.365,
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
            2.307018,
            2.779399,
            2.279982,
            2.279982,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]] * 2
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_version_1_1_should_return_version_1_0(self):
        file_name = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'cter_v1_0_multiline.txt')
        return_frame = cter.load_cter(file_name=file_name, version='1.1')

        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [[
            22257.635,
            22862.365,
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
            2.307018,
            2.779399,
            2.279982,
            2.279982,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]] * 2
        data_frame = pd.DataFrame(
            data,
            columns=columns
            )

        assert data_frame.round(5).equals(return_frame.round(5))

    def test_version_0_1_should_raise_AssertionError(self):
        file_name = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'cter_v1_0_multiline.txt')
        with pytest.raises(AssertionError):
            cter.load_cter(file_name=file_name, version='0.0')


class TestDumpCter:

    def test_valid_cter_data_version_1_0_should_create_partres_file(self, tmpdir):
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_valid_cter_data_should_create_partres_file.star')
        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [
            22257.635,
            22862.365,
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
        cter.dump_cter(output_file, data_frame, '1.0')
        assert os.path.exists(output_file)

    def test_valid_cter_data_1_0_large_angle_should_create_correct_file(self, tmpdir):
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_valid_cter_data_large_angle_should_create_correct_file.star')
        columns = (
            'DefocusU',
            'DefocusV',
            'SphericalAberration',
            'Voltage',
            'PixelSize',
            'b_factor',
            'total_ac',
            'DefocusAngle',
            'std_defocus',
            'std_total_ac',
            'std_astigmatism_amplitude',
            'std_astigmatism_angle',
            'variation_defocus',
            'variation_astigmatism_amplitude',
            'resolution_limit_defocus',
            'resolution_limit_defocus_astig',
            'nyquist',
            'CtfMaxResolution',
            'spare',
            'AmplitudeContrast',
            'PhaseShift',
            'MicrographNameNoDW'
            )
        data = [
            22257.635,
            22862.365,
            0.01,
            300,
            1.14,
            0,
            0.1,
            19.435+720,
            0.0010212,
            0,
            0.0021005,
            6.5849,
            0.045268,
            3.4734,
            2.30702,
            2.77940,
            2.27998,
            2.77940,
            0,
            0.1,
            0,
            'test_file.mrc'
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )
        cter.dump_cter(output_file, data_frame, '1.0')

        expected_data = [[
            2.256,
            0.01,
            300.0,
            1.14,
            0.0,
            10.0,
            0.060473,
            25.565 ,
            0.0010212,
            0.0,
            0.0021005,
            6.5849,
            0.045268,
            3.4734,
            0.4334596,
            0.3597899,
            0.4386003,
            0.3597899,
            0.0,
            10.0,
            0.0,
            'test_file.mrc',
            ]]
        input_data = []
        with open(output_file, 'r') as read:
            for idx, line in enumerate(read.readlines()):
                line = line.strip().split()
                input_data.append([])
                for entry in line:
                    try:
                        data = float(entry)
                    except ValueError:
                        data = entry
                    input_data[idx].append(data)

        assert expected_data == input_data
