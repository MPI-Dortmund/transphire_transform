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
        header_out = ['_a', '_b', '_c', '_d']
        assert util.create_header(names=header, index=False, prefix='') == header_out


    def test_create_header_index_list(self):
        """
        """
        header = ['a', 'b', 'c', 'd']
        header_out = ['_a #1', '_b #2', '_c #3', '_d #4']
        assert util.create_header(names=header, index=True, prefix='') == header_out


    def test_create_header_array(self):
        """
        """
        header = np.array(['a', 'b', 'c', 'd'], dtype=str)
        header_out = ['_a', '_b', '_c', '_d']
        assert util.create_header(names=header, index=False, prefix='') == header_out


    def test_create_header_index_array(self):
        """
        """
        header = np.array(['a', 'b', 'c', 'd'], dtype=str)
        header_out = ['_a #1', '_b #2', '_c #3', '_d #4']
        assert util.create_header(names=header, index=True, prefix='') == header_out


    def test_create_header_array_prefix(self):
        """
        """
        header = np.array(['a', 'b', 'c', 'd'], dtype=str)
        header_out = ['_testa', '_testb', '_testc', '_testd']
        assert util.create_header(names=header, index=False, prefix='test') == header_out


    def test_create_header_index_array_prefix(self):
        """
        """
        header = np.array(['a', 'b', 'c', 'd'], dtype=str)
        header_out = ['_testa #1', '_testb #2', '_testc #3', '_testd #4']
        assert util.create_header(names=header, index=True, prefix='test') == header_out


    def test_create_header_array_empty(self):
        """
        """
        header = np.array([], dtype=str)
        with pytest.raises(IOError):
            util.create_header(names=header, index=True, prefix='')


    def test_create_header_list_empty(self):
        """
        """
        header = []
        with pytest.raises(IOError):
            util.create_header(names=header, index=True, prefix='')


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


class TestAddToDict():

    def test_new_key_should_return_filled_dict(self):
        data_dict = {}
        key = 'a'
        value = 'b'
        util.add_to_dict(data_dict, key, value)
        assert data_dict == {'a': 'b'}

    def test_new_key_int_should_return_filled_dict(self):
        data_dict = {}
        key = 'a'
        value = 1
        util.add_to_dict(data_dict, key, value)
        assert data_dict == {'a': 1}

    def test_double_key_should_attributeerror(self):
        data_dict = {'a': 'c'}
        key = 'a'
        value = 'b'
        with pytest.raises(AttributeError):
            util.add_to_dict(data_dict, key, value)


class TestExtractFunctionFromFunctionDict:

    def dummy_function_1(self): # pragma: no cover
        pass

    def dummy_function_2(self): # pragma: no cover
        pass

    def dummy_function_3(self): # pragma: no cover
        pass

    def test_empty_version_ordered_should_return_dummy_function_3(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '1.1.2': self.dummy_function_2,
            '2.2.5': self.dummy_function_3,
            }
        assert self.dummy_function_3 == util.extract_function_from_function_dict(func_dict)

    def test_empty_version_unordered_should_return_dummy_function_3(self):
        func_dict = {
            '1.1.2': self.dummy_function_2,
            '2.2.5': self.dummy_function_3,
            '0.0.4': self.dummy_function_1,
            }
        assert self.dummy_function_3 == util.extract_function_from_function_dict(func_dict)

    def test_version_225_ordered_should_return_dummy_function_3(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '1.1.2': self.dummy_function_2,
            '2.2.5': self.dummy_function_3,
            }
        assert self.dummy_function_3 == util.extract_function_from_function_dict(func_dict, '2.2.5')

    def test_version_326_ordered_should_return_dummy_function_3(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '1.1.2': self.dummy_function_2,
            '2.2.5': self.dummy_function_3,
            }
        assert self.dummy_function_3 == util.extract_function_from_function_dict(func_dict, '3.2.6')

    def test_version_112_ordered_should_return_dummy_function_2(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '1.1.2': self.dummy_function_2,
            '2.2.5': self.dummy_function_3,
            }
        assert self.dummy_function_2 == util.extract_function_from_function_dict(func_dict, '1.1.2')

    def test_version_122_ordered_should_return_dummy_function_2(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '1.1.2': self.dummy_function_2,
            '2.2.5': self.dummy_function_3,
            }
        assert self.dummy_function_2 == util.extract_function_from_function_dict(func_dict, '1.2.2')

    def test_version_004_ordered_should_return_dummy_function_1(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '1.1.2': self.dummy_function_2,
            '2.2.5': self.dummy_function_3,
            }
        assert self.dummy_function_1 == util.extract_function_from_function_dict(func_dict, '0.0.4')

    def test_version_005_ordered_should_return_dummy_function_1(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '1.1.2': self.dummy_function_2,
            '2.2.5': self.dummy_function_3,
            }
        assert self.dummy_function_1 == util.extract_function_from_function_dict(func_dict, '0.0.5')

    def test_version_225_unordered_should_return_dummy_function_3(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        assert self.dummy_function_3 == util.extract_function_from_function_dict(func_dict, '2.2.5')

    def test_version_326_unordered_should_return_dummy_function_3(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        assert self.dummy_function_3 == util.extract_function_from_function_dict(func_dict, '3.2.6')

    def test_version_112_unordered_should_return_dummy_function_2(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        assert self.dummy_function_2 == util.extract_function_from_function_dict(func_dict, '1.1.2')

    def test_version_122_unordered_should_return_dummy_function_2(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        assert self.dummy_function_2 == util.extract_function_from_function_dict(func_dict, '1.2.2')

    def test_version_004_unordered_should_return_dummy_function_1(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        assert self.dummy_function_1 == util.extract_function_from_function_dict(func_dict, '0.0.4')

    def test_version_005_unordered_should_return_dummy_function_1(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        assert self.dummy_function_1 == util.extract_function_from_function_dict(func_dict, '0.0.5')

    def test_version_003_unordered_should_raise_AssertionError(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        with pytest.raises(AssertionError):
            util.extract_function_from_function_dict(func_dict, '0.0.3')


    def test_version_unequal_format_raises_AssertionError(self):
        func_dict = {
            '0.0.4': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        with pytest.raises(AssertionError):
            util.extract_function_from_function_dict(func_dict, '1.0')

    def test_version_unequal_format_in_keys_raises_AssertionError(self):
        func_dict = {
            '0.0': self.dummy_function_1,
            '2.2.5': self.dummy_function_3,
            '1.1.2': self.dummy_function_2,
            }
        with pytest.raises(AssertionError):
            util.extract_function_from_function_dict(func_dict, '1.0.1')

