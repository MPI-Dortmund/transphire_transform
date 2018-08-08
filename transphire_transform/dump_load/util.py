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
from typing import List, Optional, Dict, Any
import pandas as pd # type: ignore
from . import star


def create_header(names: List[str], index: bool) -> List[str]:
    """
    Create header for output file.
    An IOError is raised, if the output list is empty.

    Arguments:
    names - Header names
    index - Create indexed header

    Returns:
    List of header entries
    """
    output_list: List[str] = []
    if index:
        for idx, name in enumerate(names):
            output_list.append(f'{name} #{idx+1}')
    else:
        for name in names:
            output_list.append(name)

    if not output_list:
        raise IOError('Cannot create header from empty sequence')

    return output_list


def dump_file(
        file_name: str,
        data: pd.DataFrame,
        header: Optional[List[str]] = None,
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
        names: Optional[List[str]] = None,
        header: Optional[List[int]] = None,
        skiprows: int = 0,
        delim_whitespace: bool = True,
        **kwargs: Dict[str, Any]
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
    star_data = pd.read_csv(
        file_name,
        header=header,
        names=names,
        skiprows=skiprows,
        delim_whitespace=delim_whitespace,
        **kwargs
        )
    return star_data


def conversion_dict(export_name: str) -> Dict[str, str]:
    """
    Create a dictionary that converts internal keys to the outside world.

    Arguments:
    export_name - Specify output

    Returns:
    Dictionary for hte conversion
    """
    data_dict: Dict[str, Dict[str, str]] = {}

    return data_dict[export_name]
