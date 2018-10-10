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


def load_unblur_1_0_2(file_name: str) -> pd.DataFrame:
    """
    Read the motioncor shift files.

    Arguments:
    file_name - Name of the motioncor shift file

    Returns:
    Pandas data frame containing the extended header information
    """
    input_data: pd.DataFrame
    output_data: pd.DataFrame

    input_data = util.load_file(
        file_name,
        comment='#',
        )
    output_data = input_data.transpose()
    output_data.rename(columns={0: 'shift_x', 1: 'shift_y'}, inplace=True)
    output_data['shift_x'] -= output_data['shift_x'].iloc[0]
    output_data['shift_y'] -= output_data['shift_y'].iloc[0]

    return output_data


def load_unblur(
        file_name: str,
        version: typing.Optional[str]=None
    ) -> pd.DataFrame:
    """
    Load the unblur shift file based on the version number

    Arguments:
    file_name - Path to the input unblur file.

    Returns:
    Pnadas dataframe containing the motion information
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
        '1.0.2': load_unblur_1_0_2,
        }

    function = util.extract_function_from_function_dict(function_dict, version)
    return function(file_name)
