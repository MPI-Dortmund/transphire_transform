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


def load_eman1(file_name: str) -> pd.DataFrame:
    """
    Read the eman2 box files

    Arguments:
    file_name - Name of the box file

    Returns:
    Pandas data containing the box coordinates
    """
    output_data: pd.DataFrame

    output_data = util.load_file(
        file_name,
        names=['CoordinateX', 'CoordinateY', 'box_x', 'box_y'],
        comment='#',
        )
    output_data['CoordinateX'] += output_data['box_x'] // 2
    output_data['CoordinateY'] += output_data['box_y'] // 2

    return output_data[['CoordinateX', 'CoordinateY']]


def load_box(
        file_name: str,
        version: str
    ) -> pd.DataFrame:
    """
    Load the box file based on the version

    Arguments:
    file_name - Path to the input box file.
    version - box type

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

    function_dict = {
        'eman1': load_eman1,
        }

    return function_dict[version](file_name)
