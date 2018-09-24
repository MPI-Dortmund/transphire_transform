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
import re

import numpy as np # type: ignore
import pandas as pd # type: ignore

from . import util


def get_ctffind4_header_names() -> typing.List[str]:
    """
    Returns the header names for the ctffind4 input file.

    Arguments:
    None

    Returns:
    List of names
    """
    return [
        'defocus_u',
        'defocus_v',
        'astigmatism_angle',
        'phase_shift',
        'cross_correlation',
        'resolution_limit',
        ]


def get_ctffind4_meta(file_name: str) -> pd.DataFrame:
    """
    Import the ctffind information used.

    Arguments:
    file_name - Name of the file to export the information from.

    Returns:
    Pandas data frame containing the information.
    """
    extract_dict: typing.Dict[str, str]
    ctffind_meta_data: pd.DataFrame
    lines: typing.List[str]
    match: typing.Optional[typing.Match[str]]
    non_string_values: typing.Set[str]

    extract_dict = {
        'version': r'.*CTFFind version ([^, ]*).*',
        'micrograph_name': r'.*Input file: ([^ ]*).*',
        'pixel_size': r'.*Pixel size: ([^ ]*).*',
        'kv': r'.*acceleration voltage: ([^ ]*).*',
        'cs': r'.*spherical aberration: ([^ ]*).*',
        'ac': r'.*amplitude contrast: ([^ ]*).*',
        }
    ctffind_meta_data = pd.DataFrame(index=[0], columns=extract_dict.keys())
    with open(file_name, 'r') as read:
        lines = read.readlines()

    non_string_values = set([
        'micrograph_name',
        'version'
        ])
    for line in lines:
        for key, value in extract_dict.items():
            match = re.match(value, line)
            if match is not None:
                try:
                    ctffind_meta_data[key] = float(match.group(1))
                except ValueError:
                    assert key in non_string_values, f'{key}: {match.group(1)}'
                    ctffind_meta_data[key] = match.group(1)
            else:
                pass
    return ctffind_meta_data


def load_ctffind4(file_name: str) -> pd.DataFrame:
    """
    Load a ctffind file.

    Arguments:
    file_name - Path to the ctffind file

    Returns:
    Pandas dataframe containing the ctffind file information
    """
    header_names: typing.List[str]
    ctffind_data: pd.DataFrame
    ctffind_meta: pd.DataFrame

    header_names = get_ctffind4_header_names()
    ctffind_data = util.load_file(
        file_name,
        names=header_names,
        skiprows=5,
        usecols=(1, 2, 3, 4, 5, 6)
        )
    np.degrees(ctffind_data['phase_shift'], out=ctffind_data['phase_shift'])

    ctffind_meta = get_ctffind4_meta(file_name=file_name)
    return ctffind_data
