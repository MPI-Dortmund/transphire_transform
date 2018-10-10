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

import typing
import pandas as pd # type: ignore


def create_header(names: typing.List[str], index: bool, prefix: str) -> typing.List[str]:
    """
    Create header for output file.
    An IOError is raised, if the output list is empty.

    Arguments:
    names - Header names
    index - Create indexed header
    prefix - Star file header name prefix

    Returns:
    List of header entries
    """
    output_list: typing.List[str] = []
    if index:
        for idx, name in enumerate(names):
            output_list.append(f'_{prefix}{name} #{idx+1}')
    else:
        for name in names:
            output_list.append(f'_{prefix}{name}')

    if not output_list:
        raise IOError('Cannot create header from empty sequence')

    return output_list


def dump_file(
        file_name: str,
        data: pd.DataFrame,
        header: typing.Optional[typing.List[str]] = None,
        vertical: bool = True
    ) -> None:
    """
    Dump a file with or without a header to an output file.

    Arguments:
    file_name - Name of the output file
    data - Pandas dataframe containing the data to dump
    header - List of header names (Default None)
    vertical - Stack the header vertical or horizontal (default vertical)

    Returns:
    None
    """

    if data.empty:
        raise IOError(f'Cannot write empty data to {file_name}')

    if vertical:
        orientation = '\n'
    else:
        orientation = '\t'

    if header is None:
        export_header = ''
    else:
        export_header = '{0}\n'.format(orientation.join(header))

    with open(file_name, 'w') as write:
        write.write(f'{export_header}')
    data.to_csv(file_name, sep='\t', header=False, index=False, mode='a')


def load_file(
        file_name: str,
        names: typing.Optional[typing.List[str]] = None,
        header: typing.Optional[typing.List[int]] = None,
        skiprows: int = 0,
        delim_whitespace: bool = True,
        **kwargs: typing.Any
    ) -> pd.DataFrame:
    """
    Load the content of a file.
    Kwargs are options of the read_cvs function:
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html

    Arguments:
    file_name - Name of the file that contains the data
    header - List of header names
    skiprows - Nr of rows to skip
    delim_whitespace - Use whitespace as delimiters

    Returns:
    Pandas dataframe containing the data
    """
    load_data = pd.read_csv(
        file_name,
        header=header,
        names=names,
        skiprows=skiprows,
        delim_whitespace=delim_whitespace,
        **kwargs
        )
    return load_data


def import_keys(input_file: str) -> typing.Tuple[str, ...]:
    """
    Import

    Arguments:
    input_file - File path to the file containing the keys

    Returns:
    Tuple of keys
    """
    key_list: typing.List[str] = []
    with open(input_file, 'r') as read:
        lines: typing.List[str] = read.readlines()
    for line in lines:
        if line.strip():
            key = line.split('#')[0].strip()
            assert ' ' not in key, f'{key} is not allowed to contain whitespaces!'
            key_list.append(key)

    return tuple(key_list)


def parse_keys_to_dict(keys: typing.Tuple[str, ...], export: bool=False) -> typing.Dict[str, str]:
    """
    Create a dictionary based on the keys tuple.
    If export is True, the key, value pair will be inverted

    Arguments:
    keys - Keys tuple to parse
    export - If the keys should be there for export.

    Returns:
    Dictionary containing the keys.
    """
    output_dict: typing.Dict[str, str]
    dict_key: str
    dict_value: str
    raw_key: str
    raw_value: str

    output_dict = {}
    for key in keys:
        try:
            raw_key, raw_value = key.split(':')
        except ValueError:
            dict_key = key.strip()
            dict_value = key.strip()
        else:
            if raw_key == 'STAR_PREFIX' or not export:
                dict_key, dict_value = raw_key.strip(), raw_value.strip()
            else:
                dict_key, dict_value = raw_value.strip(), raw_key.strip()
        assert dict_key not in output_dict
        output_dict[dict_key] = dict_value

    return output_dict


def add_to_dict(data_dict: typing.Dict[str, str], key: str, value: str) -> None:
    """
    Add key, value pair to dictionary.
    Raise an AttributeError in case the key already exists in the dictionary.

    Arguments:
    data_dict - Dictionary that needs to be filled
    key - Key that needs to be added
    value - Value that needs to be added related to the key

    Returns:
    None
    """
    if key.strip() in data_dict:
        raise AttributeError(f'Key: {key} already exists in data_dict!')
    else:
        if isinstance(value, str):
            data_dict[key.strip()] = value.strip()
        else:
            data_dict[key.strip()] = value
    return None


def extract_function_from_function_dict(
        function_dict: typing.Dict[
            str,
            typing.Callable[..., typing.Any]
            ],
        version: typing.Optional[str]=None
    ) -> typing.Callable[..., typing.Any]:
    """
    Get the correct function from the function dict based on the version.
    Use the version that is closest to the specified one.

    Arguments:
    function_dict - Dictionary with the version as key and the function as argument
    version -  Version number as string in the format X.X.X.X.X....

    Returns:
    function
    """
    version_list: typing.List[typing.Tuple[int, ...]]
    match_version: typing.Tuple[int, ...]
    version_number: typing.Tuple[int, ...]
    current_version: typing.Tuple[int, ...]
    sorted_version_list: typing.List[typing.Tuple[int, ...]]
    idx_version: int

    version_list = []
    for key in function_dict:
        current_version = tuple([int(num) for num in key.split('.')])
        version_list.append(current_version)
        assert len(version_list[0]) == len(current_version)

    if version is None:
        match_version = max(version_list)

    else:
        version_number = tuple([int(num) for num in version.split('.')])
        assert len(version_number) == len(version_list[0]), \
            f'Version {version} not in the format {list(function_dict.keys())[0]}'
        version_list.append(version_number)
        sorted_version_list = sorted(version_list)
        idx_version = sorted_version_list.index(version_number)

        if idx_version == len(sorted_version_list)-1:
            match_version = sorted_version_list[idx_version-1]
        elif version_number == sorted_version_list[idx_version+1]:
            match_version = sorted_version_list[idx_version]
        elif idx_version == 0:
            assert False, f'Version {version} is too small and does not fit any key!'
        else:
            match_version = sorted_version_list[idx_version-1]

    return function_dict['.'.join([str(entry) for entry in match_version])]
