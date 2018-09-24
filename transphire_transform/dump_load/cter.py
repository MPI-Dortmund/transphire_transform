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

from . import util


def get_cter_v1_0_header_names() -> typing.List[str]:
    """
    Returns the header names for the ctffind4 input file.

    Arguments:
    None

    Returns:
    List of names
    """
    return [
        'defocus',
        'cs',
        'kv',
        'pixel_size',
        'b_factor',
        'total_ac',
        'astigmatism_amplitude',
        'astigmatism_angle',
        'std_defocus',
        'std_total_ac',
        'std_astigmatism_amplitude',
        'std_astigmatism_angle',
        'variation_defocus',
        'variation_astigmatism_amplitude',
        'resolution_limit_defocus',
        'resolution_limit',
        'nyquist',
        'spare_1',
        'spare_2',
        'ac',
        'phase_shift',
        'micrograph_name'
        ]


def load_cter_v1_0(file_name: str) -> pd.DataFrame:
    """
    Load a ctffind file.

    Arguments:
    file_name - Path to the ctffind file

    Returns:
    Pandas dataframe containing the ctffind file information
    """
    header_names: typing.List[str]
    cter_data: pd.DataFrame

    header_names = get_cter_v1_0_header_names()
    cter_data = util.load_file(
        file_name,
        names=header_names,
        )
    cter_data['ac'] = cter_data['ac'] / 100
    cter_data['total_ac'] = cter_data['total_ac'] / 100
    cter_data['astigmatism_angle'] = 45 - cter_data['astigmatism_angle']

    defocus_data = pd.DataFrame(index=[0], columns=('defocus_u', 'defocus_v'))
    defocus_data['defocus_u'], defocus_data['defocus_v'] = defocus_defocus_diff_to_defocus_u_and_v(
        cter_data['defocus'],
        cter_data['astigmatism_amplitude']
        )
    cter_data_dropped = cter_data.drop(labels=['defocus', 'astigmatism_amplitude'], axis=1)

    return pd.concat([defocus_data, cter_data_dropped], axis=1)


def defocus_defocus_diff_to_defocus_u_and_v(
        defocus: pd.Series,
        astigmatism: pd.Series
    ) -> typing.Tuple[pd.Series, pd.Series]:
    """
    Calculate the defocus_u and defocus_v value based on the average defocus
    and the difference between the two values.

    Arguments:
    defocus - Average defocus value
    astigmatism - Difference between the two defocus values (astigmatism amplitude)

    Returns:
    Defocus_U and Defocus_V
    """
    defocus_u: pd.Series
    defocus_v: pd.Series

    defocus_v = (20000*defocus - 10000*astigmatism) / 2
    defocus_u = 20000*defocus - defocus_v
    return defocus_u, defocus_v
