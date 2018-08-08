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
from typing import List, Tuple
import pandas as pd # type: ignore
from . import util


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
    output_list.extend(util.create_header(names=names, index=True))
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
    header: List[str] = create_star_header(names=data.keys())
    util.dump_file(
        file_name=file_name,
        data=data,
        header=header,
        vertical=True
        )


def load_star_header(file_name: str) -> Tuple[List[str], int]:
    """
    Load the header information.

    Arguments:
    file_name - Path to the file that contains the header.

    Returns:
    List of header names, rows that are occupied by the header.
    """
    start_header: bool = False
    header_names: List[str] = []
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
    Load a relion star file.

    Arguments:
    file_name - Path to the relion star file

    Returns:
    Pandas dataframe containing the star file
    """
    header_names: List[str]
    skip_index: int
    star_data: pd.DataFrame

    header_names, skip_index = load_star_header(file_name=file_name)
    star_data = util.load_file(file_name, names=header_names, skiprows=skip_index)
    return star_data
