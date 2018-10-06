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

import re
import os
import glob
import typing
import pandas as pd # type: ignore
from . import util

FILE_DIRECTORY: str = os.path.dirname(os.path.realpath(__file__))

def create_star_header(names: typing.List[str], prefix: str) -> typing.List[str]:
    """
    Create a header for a star file.

    Arguments:
    names - List or array of header names
    prefix - Star file header name prefix

    Returns:
    Header string
    """
    output_list: typing.List[str] = [
        '',
        'data_',
        '',
        'loop_',
        ]
    output_list.extend(util.create_header(names=names, index=True, prefix=prefix))
    return output_list


def dump_star(file_name: str, data: pd.DataFrame, version: str) -> None:
    """
    Create a star file.

    Arguments:
    file_name - File name to export
    data - Data to export
    version - output version string

    Returns:
    None
    """
    header: typing.List[str]
    new_header: typing.List[str]
    old_header: typing.List[str]
    prefix: str

    new_header, old_header, prefix = \
        export_star_header(header_names=data.keys(), version=version)
    header = create_star_header(names=new_header, prefix=prefix)
    util.dump_file(
        file_name=file_name,
        data=data[old_header],
        header=header,
        vertical=True
        )


def load_star_header(file_name: str) -> typing.Tuple[typing.List[str], int]:
    """
    Load the header information.

    Arguments:
    file_name - Path to the file that contains the header.

    Returns:
    List of header names, rows that are occupied by the header.
    """
    start_header: bool = False
    header_names: typing.List[str] = []
    idx: int

    with open(file_name, 'r') as read:
        for idx, line in enumerate(read.readlines()):
            if line.startswith('_'):
                if start_header:
                    header_names.append(line.strip().split()[0])
                else:
                    start_header = True
                    header_names.append(line.strip().split()[0])
            elif start_header:
                break

    if not start_header:
        raise IOError(f'No header information found in {file_name}')

    return header_names, idx


def load_star(file_name: str) -> pd.DataFrame:
    """
    Load a star file.

    Arguments:
    file_name - Path to the star file

    Returns:
    Pandas dataframe containing the star file
    """
    header_names: typing.List[str]
    import_names: typing.List[str]
    skip_index: int
    star_data: pd.DataFrame

    header_names, skip_index = load_star_header(file_name=file_name)
    import_names = import_star_header(header_names=header_names)
    star_data = util.load_file(file_name, names=import_names, skiprows=skip_index)
    return star_data


def import_star_header(header_names: typing.List[str]) -> typing.List[str]:
    """
    Get the header keys.
    Detect the star version automatically.

    Arguments:
    header_names - star file header.

    Returns:
    List of new keys
    """
    key_files: typing.List[str]
    star_version: typing.Dict[str, typing.Dict[str, str]]
    version_match: typing.Pattern
    versions: typing.Optional[typing.List[str]]
    key_match: typing.Optional[typing.Match[str]]
    import_dict: typing.Dict[str, str]
    output_header: typing.List[str]

    key_files = glob.glob(os.path.join(FILE_DIRECTORY, 'keys', 'star_keys_*.txt'))
    star_version = {}
    version_match = re.compile(r'.*star_keys_(.*)\.txt')
    versions = None
    key_match = None

    for file_name in sorted(key_files):
        key_match = version_match.match(file_name)
        assert key_match is not None
        star_version[key_match.group(1)] = util.parse_keys_to_dict(util.import_keys(file_name))

    for name in header_names:
        versions = []

        for key, value in star_version.items():
            if name.lstrip(f'_{value["STAR_PREFIX"]}') in value:
                versions.append(key)

        if not versions:
            assert False, f'Star key not known in present versions: {name}'
        elif len(versions) == 1:
            break
    assert versions is not None, f'Header names is empty!'

    output_header = []
    import_dict = star_version[versions[-1]]
    for name in header_names:
        output_header.append(import_dict[name.lstrip(f'_{import_dict["STAR_PREFIX"]}')])

    return output_header


def export_star_header(
        header_names: typing.List[str],
        version: str
    ) -> typing.Tuple[typing.List[str], typing.List[str], str]:
    """
    Get the header keys.

    Arguments:
    header_names - star file header.
    version - Output star file version

    Returns:
    List of new keys, List of valid old keys, prefix
    """
    key_tuple: typing.Tuple[str, ...]
    output_header: typing.List[str]
    old_header_values: typing.List[str]
    export_dict: typing.Dict[str, str]

    key_tuple = util.import_keys(
        os.path.join(FILE_DIRECTORY, 'keys', f'star_keys_{version}.txt')
        )
    export_dict = util.parse_keys_to_dict(key_tuple, export=True)

    output_header = []
    old_header_values = []
    for name in header_names:
        try:
            new_name = export_dict[name]
        except KeyError:
            continue
        else:
            output_header.append(new_name)
            old_header_values.append(name)

    assert output_header
    assert old_header_values

    return output_header, old_header_values, export_dict['STAR_PREFIX']
