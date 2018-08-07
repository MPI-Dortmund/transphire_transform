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
from typing import List
import pandas as pd
from . import load_dump_util


def create_star_header(names: List[str]) -> List[str]:
    """
    Create a header for a relion star file.

    Arguments:
    names - List or array of header names

    Returns:
    Header string
    """
    output_list: List[str] = [
        '',
        'data_',
        '',
        'loop_',
        ]
    output_list.extend(dump_load_util.create_header(names=names, index=True))
    return output_list


def dump_star(file_name: str, data: pd.DataFrame) -> None:
    """
    Create a relion star file.

    Arguments:
    file_name - File name to export
    data - Data to export

    Returns:
    None
    """
    if data.empty:
        raise IOError(f'Cannot write empty data to ${file_name}')
    header: List[str] = create_star_header(names=data.keys())
    dump_load_util.dump_file(
        file_name=file_name,
        data=data,
        header=header,
        vertical=True
        )
