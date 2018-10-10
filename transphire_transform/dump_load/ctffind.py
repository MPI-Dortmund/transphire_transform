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


def get_ctffind_4_1_0_header_names() -> typing.List[str]:
    """
    Returns the header names for the ctffind4 input file.

    Arguments:
    None

    Returns:
    List of names
    """
    return [
        'DefocusU',
        'DefocusV',
        'DefocusAngle',
        'PhaseShift',
        'CtfFigureOfMerit',
        'CtfMaxResolution',
        ]


def get_ctffind_4_1_0_extract_dict() -> typing.Dict[str, str]:
    """
    Returns the extraction dict for the ctffind4 meta information.

    Arguments:
    None

    Returns:
    Dictionary with key as key and regular expression as value.
    """
    return {
        'version': r'.*CTFFind version ([^, ]*).*',
        'MicrographNameNoDW': r'.*Input file: ([^ ]*).*',
        'PixelSize': r'.*Pixel size: ([^ ]*).*',
        'Voltage': r'.*acceleration voltage: ([^ ]*).*',
        'SphericalAberration': r'.*spherical aberration: ([^ ]*).*',
        'AmplitudeContrast': r'.*amplitude contrast: ([^ ]*).*',
        }


def get_ctffind_4_1_0_meta(file_name: str) -> pd.DataFrame:
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

    extract_dict = get_ctffind_4_1_0_extract_dict()
    ctffind_meta_data = pd.DataFrame(index=[0], columns=extract_dict.keys())
    with open(file_name, 'r') as read:
        lines = read.readlines()

    non_string_values = set([
        'MicrographNameNoDW',
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


def load_ctffind_4_1_0(file_name: str) -> pd.DataFrame:
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

    header_names = get_ctffind_4_1_0_header_names()
    ctffind_data = util.load_file(
        file_name,
        names=header_names,
        skiprows=5,
        usecols=(1, 2, 3, 4, 5, 6)
        )
    ctffind_data['PhaseShift'] = np.degrees(ctffind_data['PhaseShift'])

    ctffind_meta = get_ctffind_4_1_0_meta(file_name=file_name)
    return pd.concat([ctffind_data, ctffind_meta], axis=1)


def load_ctffind(
        file_name: str,
        version: typing.Optional[str]=None
    ) -> pd.DataFrame:
    """
    Create a cter partres file based on the cter_data information.
    By default, the latest cter version is assumed.

    Arguments:
    file_name - Path to the output partres file.
    version - Cter version default the latest version

    Returns:
    Pandas dataframe containing the ctffind file information
    """
    function_dict: typing.Dict[
        str,
        typing.Callable[
            [str],
            pd.DataFrame
            ]
        ]
    function: typing.Callable[[str], pd.DataFrame]

    function_dict = {
        '4.1.0': load_ctffind_4_1_0,
        }

    function = util.extract_function_from_function_dict(function_dict, version)
    return function(file_name)
