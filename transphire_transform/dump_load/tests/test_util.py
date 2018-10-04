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

import numpy as np
import pandas as pd
import pytest
from .. import util


OUTPUT_TEST_FOLDER = 'OUTPUT_TESTS_LOAD_DUMP_UTIL'


class TestCreateHeader:
    def test_create_header_list(self):
        """
        """
        header = ['a', 'b', 'c', 'd']
        assert util.create_header(names=header, index=False) == header


    def test_create_header_index_list(self):
        """
        """
        header = ['a', 'b', 'c', 'd']
        header_out = ['a #1', 'b #2', 'c #3', 'd #4']
        assert util.create_header(names=header, index=True) == header_out


    def test_create_header_array(self):
        """
        """
        header = np.array(['a', 'b', 'c', 'd'], dtype=str)
        assert util.create_header(names=header, index=False) == header.tolist()


    def test_create_header_index_array(self):
        """
        """
        header = np.array(['a', 'b', 'c', 'd'], dtype=str)
        header_out = ['a #1', 'b #2', 'c #3', 'd #4']
        assert util.create_header(names=header, index=True) == header_out


    def test_create_header_array_empty(self):
        """
        """
        header = np.array([], dtype=str)
        with pytest.raises(IOError):
            util.create_header(names=header, index=True)


    def test_create_header_list_empty(self):
        """
        """
        header = []
        with pytest.raises(IOError):
            util.create_header(names=header, index=True)


class TestDumpFile:
    def test_dump_file_empty(self, tmpdir):
        """
        """
        data = pd.DataFrame({
            })
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_empty')
        with pytest.raises(IOError):
            util.dump_file(
                file_name=output_file,
                data=data,
                header=None,
                vertical=True,
                )


    def test_dump_file_four(self, tmpdir):
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
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_four')
        util.dump_file(
            file_name=output_file,
            data=data,
            header=None,
            vertical=True,
            )
        load_data = util.load_file(file_name=output_file)
        assert np.array_equal(load_data.values, data.values)


    def test_dump_file_single(self, tmpdir):
        """
        """
        data_1 = np.arange(4)
        data = pd.DataFrame({
            '_rlnTest1': data_1,
            })
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_single')
        util.dump_file(
            file_name=output_file,
            data=data,
            header=None,
            vertical=True,
            )
        load_data = util.load_file(file_name=output_file)
        assert np.array_equal(load_data.values, data.values)


    def test_dump_file_four_hor(self, tmpdir):
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
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_four_hor')
        util.dump_file(
            file_name=output_file,
            data=data,
            header=None,
            vertical=False,
            )
        load_data = util.load_file(file_name=output_file)
        assert np.array_equal(load_data.values, data.values)


    def test_dump_file_single_hor(self, tmpdir):
        """
        """
        data_1 = np.arange(4)
        data = pd.DataFrame({
            '_rlnTest1': data_1,
            })
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_single_hor')
        util.dump_file(
            file_name=output_file,
            data=data,
            header=None,
            vertical=False,
            )
        load_data = util.load_file(file_name=output_file)
        assert np.array_equal(load_data.values, data.values)


    def test_dump_file_four_header(self, tmpdir):
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
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_four')
        util.dump_file(
            file_name=output_file,
            data=data,
            header=data.keys(),
            vertical=True,
            )
        assert util.load_file(file_name=output_file, names=data.keys(), skiprows=4).equals(data)


    def test_dump_file_single_header(self, tmpdir):
        """
        """
        data_1 = np.arange(4)
        data = pd.DataFrame({
            '_rlnTest1': data_1,
            })
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_single')
        util.dump_file(
            file_name=output_file,
            data=data,
            header=data.keys(),
            vertical=True,
            )
        assert util.load_file(file_name=output_file, names=data.keys(), skiprows=1).equals(data)


    def test_dump_file_four_hor_header(self, tmpdir):
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
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_four_hor')
        util.dump_file(
            file_name=output_file,
            data=data,
            header=None,
            vertical=False,
            )
        util.dump_file(
            file_name=output_file,
            data=data,
            header=data.keys(),
            vertical=False,
            )
        assert util.load_file(file_name=output_file, names=data.keys(), skiprows=1).equals(data)


    def test_dump_file_single_hor_header(self, tmpdir):
        """
        """
        data_1 = np.arange(4)
        data = pd.DataFrame({
            '_rlnTest1': data_1,
            })
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_dump_file_single_hor')
        util.dump_file(
            file_name=output_file,
            data=data,
            header=None,
            vertical=False,
            )
        util.dump_file(
            file_name=output_file,
            data=data,
            header=data.keys(),
            vertical=False,
            )
        assert util.load_file(file_name=output_file, names=data.keys(), skiprows=1).equals(data)

class TestImportKeys:

    def test_import_keys_filled_file_should_work(self, tmpdir):
        """
        """
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_import_keys_filled_file_should_work')
        keys = ('test_a', 'test_b', 'test_c')
        suffix = ('test', 'test2', 'test3')
        with open(output_file, 'w') as w:
            for key, suf in zip(keys, suffix):
                w.write(f'{key} # {suf}\n')

        imported_keys = util.import_keys(output_file)
        assert keys == imported_keys

    def test_import_keys_filled_file_multi_hastag_should_work(self, tmpdir):
        """
        """
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_import_keys_filled_file_multi_hastag_should_work')
        keys = ('test_a', 'test_b', 'test_c')
        suffix = ('test', 'test2', 'test3')
        with open(output_file, 'w') as w:
            for key, suf in zip(keys, suffix):
                w.write(f'{key} # TEST1 # {suf}\n')

        imported_keys = util.import_keys(output_file)
        assert keys == imported_keys

    def test_import_keys_empty_file_should_work(self, tmpdir):
        """
        """
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_import_keys_empty_file_should_work')
        keys = ()
        suffix = ()
        with open(output_file, 'w') as w:
            pass

        imported_keys = util.import_keys(output_file)
        assert keys == imported_keys

    def test_import_keys_contains_whitespace_should_raise_AssertError(self, tmpdir):
        """
        """
        output_file: str = tmpdir.mkdir(OUTPUT_TEST_FOLDER).join('test_import_keys_contains_whitespace_should_raise_AssertError')
        keys = ()
        suffix = ()
        keys = ('test_a', 'test_b', 'test_c')
        suffix = ('test', 'test2', 'test3')
        with open(output_file, 'w') as w:
            for key, suf in zip(keys, suffix):
                w.write(f'{key} TEST1 # {suf}\n')

        with pytest.raises(AssertionError):
            util.import_keys(output_file)


class TestParseKeysToDict:

    def test_input_unspecified_to_output(self):
        data = ('test',)
        data_output = {'test': 'test'}
        data_return = util.parse_keys_to_dict(data)
        assert data_output == data_return

    def test_input_unspecified_export_to_output(self):
        data = ('test',)
        data_output = {'test': 'test'}
        data_return = util.parse_keys_to_dict(data, True)
        assert data_output == data_return

    def test_input_specified_to_output(self):
        data = ('test:test2',)
        data_output = {'test': 'test2'}
        data_return = util.parse_keys_to_dict(data)
        assert data_output == data_return

    def test_input_specified_export_to_output(self):
        data = ('test:test2',)
        data_output = {'test2': 'test'}
        data_return = util.parse_keys_to_dict(data, True)
        assert data_output == data_return
