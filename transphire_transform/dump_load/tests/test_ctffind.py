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
INPUT_TEST_FOLDER = '../../../test_files'

@pytest.fixture('module')
def ctffind_4_1_0_file():
    return os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'ctffind.txt')

@pytest.fixture('module')
def ctffind_4_1_0_meta():
    return 1.090, 300.0, 0.01, 0.07, 'test_file.mrc', '4.1.10'

@pytest.fixture('module')
def ctffind_4_1_0_data():
    return 19234.876953, 18202.244141, -62.292507, 0.000000, 0.036304, 3.604121

class TestGetCtffind410HeaderNames:

    def test_call_functions_returns_list(self):
        values = [
            'DefocusU',
            'DefocusV',
            'DefocusAngle',
            'PhaseShift',
            'CtfFigureOfMerit',
            'CtfMaxResolution',
            ]
        assert ctffind.get_ctffind_4_1_0_header_names() == values


class TestGetCtffind410Meta:

    def test_correct_file_should_return_filled_data_frame(self, ctffind_4_1_0_meta, ctffind_4_1_0_file):
        apix, kv, cs, ac, file_name, version = ctffind_4_1_0_meta
        data_frame = pd.DataFrame(
            [[version, file_name, apix, kv, cs, ac]],
            columns=(
                'version',
                'MicrographNameNoDW',
                'PixelSize',
                'Voltage',
                'SphericalAberration',
                'AmplitudeContrast'
                )
            )
        return_frame = ctffind.get_ctffind_4_1_0_meta(ctffind_4_1_0_file)
        assert data_frame.equals(return_frame)

    def test_corrupt_file_should_raise_assertionerror(self):
        with pytest.raises(AssertionError):
            return_frame = ctffind.get_ctffind_4_1_0_meta(os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'ctffind_corrupt.txt'))


class TestLoadCtffind410:

    def test_correct_file_should_return_filled_data_frame(self, ctffind_4_1_0_meta, ctffind_4_1_0_file, ctffind_4_1_0_data):
        apix, kv, cs, ac, file_name, version = ctffind_4_1_0_meta
        def_1, def_2, ast_ang, vpp, cc, limit = ctffind_4_1_0_data
        columns = (
            'DefocusU',
            'DefocusV',
            'DefocusAngle',
            'PhaseShift',
            'CtfFigureOfMerit',
            'CtfMaxResolution',
            'version',
            'MicrographNameNoDW',
            'PixelSize',
            'Voltage',
            'SphericalAberration',
            'AmplitudeContrast'
            )
        data = [
            def_1,
            def_2,
            ast_ang,
            vpp,
            cc,
            limit,
            version,
            file_name,
            apix,
            kv,
            cs,
            ac
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )
        return_frame = ctffind.load_ctffind_4_1_0(ctffind_4_1_0_file)
        assert data_frame.equals(return_frame.round(6))

    def test_corrupt_file_should_raise_assertionerror(self):
        ctffind_4_1_0_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'ctffind_corrupt.txt')
        with pytest.raises(AssertionError):
            return_frame = ctffind.load_ctffind_4_1_0(ctffind_4_1_0_file)

class TestLoadCtffind:

    def test_correct_file_4_1_0_should_return_filled_data_frame(self, ctffind_4_1_0_meta, ctffind_4_1_0_file, ctffind_4_1_0_data):
        apix, kv, cs, ac, file_name, version = ctffind_4_1_0_meta
        def_1, def_2, ast_ang, vpp, cc, limit = ctffind_4_1_0_data
        columns = (
            'DefocusU',
            'DefocusV',
            'DefocusAngle',
            'PhaseShift',
            'CtfFigureOfMerit',
            'CtfMaxResolution',
            'version',
            'MicrographNameNoDW',
            'PixelSize',
            'Voltage',
            'SphericalAberration',
            'AmplitudeContrast'
            )
        data = [
            def_1,
            def_2,
            ast_ang,
            vpp,
            cc,
            limit,
            version,
            file_name,
            apix,
            kv,
            cs,
            ac
            ]
        data_frame = pd.DataFrame(
            [data],
            columns=columns
            )
        return_frame = ctffind.load_ctffind(ctffind_4_1_0_file, '4.1.0')
        assert data_frame.equals(return_frame.round(6))

    def test_corrupt_file_should_raise_assertionerror(self):
        ctffind_4_1_0_file = os.path.join(THIS_DIR, INPUT_TEST_FOLDER, 'ctffind_corrupt.txt')
        with pytest.raises(AssertionError):
            return_frame = ctffind.load_ctffind_4_1_0(ctffind_4_1_0_file)

