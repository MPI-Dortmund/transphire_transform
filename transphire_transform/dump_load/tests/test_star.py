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


import pytest
import pandas as pd
import numpy as np
from .. import star


OUTPUT_TEST_FOLDER = 'OUTPUT_TESTS_DUMP'


class TestStarHeader:
    def test_create_star_header_four_list(self):
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

        assert star.create_star_header(names=header_names) == expected_output


    def test_create_star_header_four_array(self):
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

        assert star.create_star_header(names=header_names) == expected_output


    def test_create_star_header_single_list(self):
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

        assert star.create_star_header(names=header_names) == expected_output


    def test_create_star_header_single_array(self):
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

        assert star.create_star_header(names=header_names) == expected_output


class TestDumpStar:
    def test_dump_star_four(self, tmpdir):
        """
        """
        data_1 = np.arange(4)
        data_2 = ['a', 'b', 'c', 'd']
        data_3 = np.array(np.arange(4), dtype=float)
        data_4 = [1]*4
        data = pd.DataFrame({
            '_rlnMicrographName': data_1,
            '_rlnImageName': data_2,
            '_rlnCoordinateX': data_3,
            '_rlnCoordinateY': data_4,
            })

        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_star_four.star')
        star.dump_star(file_name=output_file, data=data, version='relion_2')
        assert star.load_star(file_name=output_file).equals(data)


    def test_dump_star_single(self, tmpdir):
        """
        """
        data_1 = np.arange(4)
        data = pd.DataFrame({
            '_rlnCoordinateX': data_1,
            })

        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_star_single.star')
        star.dump_star(file_name=output_file, data=data, version='relion_2')
        assert star.load_star(file_name=output_file).equals(data)


    def test_dump_star_single_empty(self, tmpdir):
        """
        """
        data = pd.DataFrame({
            })

        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_star_single_empty.star')
        with pytest.raises(AssertionError):
            star.dump_star(file_name=output_file, data=data, version='relion_2')


class TestLoadStarHeader:
    def test_load_star_header_single(self, tmpdir):
        data_1 = np.arange(4)
        data = pd.DataFrame({
            '_rlnMicrographName': data_1,
            })

        output_file = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_load_star_header_single.star')
        star.dump_star(file_name=output_file, data=data, version='relion_2')
        assert star.load_star_header(file_name=output_file) == (data.keys().tolist(), 5)


    def test_load_star_header_four(self, tmpdir):
        data_1 = np.arange(4)
        data_2 = ['a', 'b', 'c', 'd']
        data_3 = np.array(np.arange(4), dtype=float)
        data_4 = [1]*4
        data = pd.DataFrame({
            '_rlnMicrographName': data_1,
            '_rlnImageName': data_2,
            '_rlnCoordinateX': data_3,
            '_rlnCoordinateY': data_4,
            })

        output_file = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_load_star_header_four.star')
        star.dump_star(file_name=output_file, data=data, version='relion_2')
        assert star.load_star_header(file_name=output_file) == (data.keys().tolist(), 8)


class TestLoadStar:
    def test_load_star_single(self, tmpdir):
        data_1 = np.arange(4)
        data = pd.DataFrame({
            '_rlnMicrographName': data_1,
            })

        output_file = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_load_star_single.star')
        star.dump_star(file_name=output_file, data=data, version='relion_2')
        assert star.load_star(file_name=output_file).equals(data)


    def test_load_star_four(self, tmpdir):
        data_1 = np.arange(4)
        data_2 = ['a', 'b', 'c', 'd']
        data_3 = np.array(np.arange(4), dtype=float)
        data_4 = [1]*4
        data = pd.DataFrame({
            '_rlnMicrographName': data_1,
            '_rlnImageName': data_2,
            '_rlnCoordinateX': data_3,
            '_rlnCoordinateY': data_4,
            })

        output_file = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_load_star_four.star')
        star.dump_star(file_name=output_file, data=data, version='relion_2')
        assert star.load_star(file_name=output_file).equals(data)


    def test_load_star_single_empty(self, tmpdir):
        """
        """

        output_file = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_load_star_single_empty.star')
        with open(output_file, 'w'):
            pass
        with pytest.raises(IOError):
            star.load_star(file_name=output_file)


class TestImportStarHeader:

    def test_MicrographName_outputs_MicrographName(self):
        """
        """
        out_dict = star.import_star_header(['_rlnMicrographName'])
        assert ['_rlnMicrographName'] == out_dict

    def test_SgdSkipAnneal_outputs_SgdSkipAnneal(self):
        """
        """
        out_dict = star.import_star_header(['_rlnSgdSkipAnneal'])
        assert ['_rlnSgdSkipAnneal'] == out_dict

    def test_SgdNextSubset_outputs_SgdNextSubset(self):
        """
        """
        out_dict = star.import_star_header(['_rlnSgdNextSubset'])
        assert ['_rlnSgdNextSubset'] == out_dict

    def test_testii_raises_AssertionError(self):
        """
        """
        with pytest.raises(AssertionError):
            star.import_star_header(['testii'])

    def test_empty_header_raises_AssertionError(self):
        """
        """
        with pytest.raises(AssertionError):
            star.import_star_header([])


class TestExportStarHeader:

    def test_input_relion2_outputs_relion2_correct_out_header(self):
        out_header, _ = star.export_star_header(
            ['_rlnMicrographName', '_rlnSgdNextSubset'],
            version='relion_2'
            )
        assert ['_rlnMicrographName', '_rlnSgdNextSubset'] == out_header

    def test_input_relion2_outputs_relion2_correct_old_header(self):
        _, old_header = star.export_star_header(
            ['_rlnMicrographName', '_rlnSgdNextSubset'],
            version='relion_2'
            )
        assert ['_rlnMicrographName', '_rlnSgdNextSubset'] == old_header

    def test_input_relion2_outputs_relion3_correct_out_header(self):
        out_header, _ = star.export_star_header(
            ['_rlnMicrographName', '_rlnSgdNextSubset'],
            version='relion_3'
            )
        assert ['_rlnMicrographName'] == out_header

    def test_input_relion2_outputs_relion3_correct_old_header(self):
        _, old_header = star.export_star_header(
            ['_rlnMicrographName', '_rlnSgdNextSubset'],
            version='relion_3'
            )
        assert ['_rlnMicrographName'] == old_header
