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
import numpy as np
from .. import dump_star
from ...load import load_star


OUTPUT_TEST_FOLDER = 'OUTPUT_TESTS_DUMP'


def test_create_star_header_four_list():
    """
    """
    header_names = [
        '_rlnTest1',
        '_rlnTest2',
        '_rlnTest3',
        '_pipeTest4',
        ]

    expected_output = [
        '',
        'data_',
        '',
        'loop_',
        '_rlnTest1 #1',
        '_rlnTest2 #2',
        '_rlnTest3 #3',
        '_pipeTest4 #4',
        ]

    assert dump_star.create_star_header(names=header_names) == '\n'.join(expected_output)


def test_create_star_header_four_array():
    """
    """
    header_names = np.array([
        '_rlnTest1',
        '_rlnTest2',
        '_rlnTest3',
        '_pipeTest4',
        ], dtype=str)

    expected_output = [
        '',
        'data_',
        '',
        'loop_',
        '_rlnTest1 #1',
        '_rlnTest2 #2',
        '_rlnTest3 #3',
        '_pipeTest4 #4',
        ]

    assert dump_star.create_star_header(names=header_names) == '\n'.join(expected_output)


def test_create_star_header_single_list():
    """
    """
    header_names = [
        '_rlnTest1',
        ]

    expected_output = [
        '',
        'data_',
        '',
        'loop_',
        '_rlnTest1 #1',
        ]

    assert dump_star.create_star_header(names=header_names) == '\n'.join(expected_output)


def test_create_star_header_single_array():
    """
    """
    header_names = np.array([
        '_rlnTest1',
        ], dtype=str)

    expected_output = [
        '',
        'data_',
        '',
        'loop_',
        '_rlnTest1 #1',
        ]

    assert dump_star.create_star_header(names=header_names) == '\n'.join(expected_output)


def test_dump_star_four(tmpdir):
    """
    """
    data_1 = np.arange(4)
    data_2 = ['a', 'b', 'c', 'd']
    data_3 = np.array(np.arange(4), dtype=float)
    data_4 = [1]*4
    data = pd.DataFrame({
        '_rlnTest1': data_1,
        '_rlnTest2': data_2,
        '_rlnTest3': data_3,
        '_pipeTest4': data_4,
        })

    output_file = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_star_four.star')
    dump_star.dump_star(file_name=output_file, data=data)
    assert load_star.load_star(file_name=output_file).equals(data)


def test_dump_star_single(tmpdir):
    """
    """
    data_1 = np.arange(4)
    data = pd.DataFrame({
        '_rlnTest1': data_1,
        })

    output_file = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_star_single.star')
    dump_star.dump_star(file_name=output_file, data=data)
    assert load_star.load_star(file_name=output_file).equals(data)
