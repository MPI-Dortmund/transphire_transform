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
from typing import List, Optional
import pandas as pd


def create_header(names: List[str], index: bool) -> List[str]:
    """
    Create header for output file.

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
