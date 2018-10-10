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

import numpy as np # type: ignore
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
        'SphericalAberration',
        'Voltage',
        'PixelSize',
        'b_factor',
        'total_ac',
        'astigmatism_amplitude',
        'DefocusAngle',
        'std_defocus',
        'std_total_ac',
        'std_astigmatism_amplitude',
        'std_astigmatism_angle',
        'variation_defocus',
        'variation_astigmatism_amplitude',
        'resolution_limit_defocus',
        'resolution_limit_defocus_astig',
        'nyquist',
        'CtfMaxResolution',
        'spare',
        'AmplitudeContrast',
        'PhaseShift',
        'MicrographNameNoDW'
        ]


def load_cter(
        file_name: str,
        version: typing.Optional[str]=None
    ) -> None:
    """
    Create a cter partres file based on the cter_data information.
    By default, the latest cter version is assumed.

    Arguments:
    file_name - Path to the output partres file.
    version - Cter version default the latest version

    Returns:
    None
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
        '1.0': load_cter_v1_0,
        }

    function = util.extract_function_from_function_dict(function_dict, version)
    return function(file_name)


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

    defocus_data, cter_data_dropped = cter_to_intern(cter_data=cter_data)

    return pd.concat([defocus_data, cter_data_dropped], axis=1)


def dump_cter(
        file_name: str,
        cter_data: pd.DataFrame,
        version: typing.Optional[str]=None
    ) -> None:
    """
    Create a cter partres file based on the cter_data information.
    By default, the latest cter version is assumed.

    Arguments:
    file_name - Path to the output partres file.
    cter_data - Pandas data frame containing ctf information.
    version - Cter version default the latest version

    Returns:
    None
    """
    function_dict: typing.Dict[
        str,
        typing.Callable[
            [str, pd.DataFrame],
            None
            ]
        ]
    function: typing.Callable[[str, pd.DataFrame], None]

    function_dict = {
        '1.0': dump_cter_v1_0,
        }

    function = util.extract_function_from_function_dict(function_dict, version)
    return function(file_name, cter_data)


def dump_cter_v1_0(file_name: str, cter_data: pd.DataFrame) -> None:
    """
    Create a cter v1.0 partres file based on the cter_data information.

    Arguments:
    file_name - Path to the output partres file.
    cter_data - Pandas data frame containing ctf information.

    Returns:
    None
    """
    cter_header_names: typing.List[str]
    cter_valid_list: typing.List[str]
    defocus_frame: pd.DataFrame
    output_frame: pd.DataFrame

    cter_valid_list = []
    cter_header_names = get_cter_v1_0_header_names()
    for column_name in cter_data.columns.values:
        if column_name in cter_header_names:
            cter_valid_list.append(column_name)

    defocus_frame = pd.DataFrame(
        index=range(len(cter_data)),
        columns=('defocus', 'astigmatism_amplitude')
        )

    defocus_frame['defocus'], defocus_frame['astigmatism_amplitude'] = \
        defocus_u_and_v_to_defocus_defocus_diff(
            cter_data['DefocusU'],
            cter_data['DefocusV']
            )

    output_frame = pd.DataFrame(
        0,
        index=range(len(cter_data)),
        columns=cter_header_names
        )

    for data_frame in [cter_data, defocus_frame]:
        for header_name in cter_header_names:
            try:
                output_frame[header_name] = data_frame[header_name]
            except KeyError:
                pass

    intern_to_cter(cter_data=output_frame, valid_list=cter_valid_list)

    util.dump_file(file_name=file_name, data=output_frame.round(7))


def cter_to_intern(cter_data: pd.DataFrame) -> typing.Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convert the necessary values from cter format to internal mrc format.

    Arguments:
    cter_data - Data containing the raw information.

    Returns:
    None
    """
    cter_data['AmplitudeContrast'] = cter_data['AmplitudeContrast'] / 100
    cter_data['total_ac'] = cter_data['total_ac'] / 100
    cter_data['DefocusAngle'] = 45 - cter_data['DefocusAngle']

    cter_data['nyquist'] = 1 / cter_data['nyquist']
    cter_data['resolution_limit_defocus_astig'] = 1 / cter_data['resolution_limit_defocus_astig']
    cter_data['resolution_limit_defocus'] = 1 / cter_data['resolution_limit_defocus']
    cter_data['CtfMaxResolution'] = 1 / cter_data['CtfMaxResolution']

    mask = (cter_data['DefocusAngle'] < 0)
    while mask.any():
        cter_data.loc[mask, 'DefocusAngle'] += 180
        mask = (cter_data['DefocusAngle'] < 0)

    mask = (cter_data['DefocusAngle'] >= 180)
    while mask.any():
        cter_data.loc[mask, 'DefocusAngle'] -= 180
        mask = (cter_data['DefocusAngle'] >= 180)

    defocus_data = pd.DataFrame(
        index=range(len(cter_data)),
        columns=('DefocusU', 'DefocusV')
        )
    defocus_data['DefocusU'], defocus_data['DefocusV'] = \
        defocus_defocus_diff_to_defocus_u_and_v(
            cter_data['defocus'],
            cter_data['astigmatism_amplitude']
            )
    cter_data_dropped = cter_data.drop(labels=['defocus', 'astigmatism_amplitude'], axis=1)
    return defocus_data, cter_data_dropped


def intern_to_cter(cter_data: pd.DataFrame, valid_list: typing.List[str]) -> None:
    """
    Convert the necessary values from cter format to internal mrc format.

    Arguments:
    cter_data - Data containing the raw information.

    Returns:
    None
    """
    mask: pd.Series

    cter_data['AmplitudeContrast'] = cter_data['AmplitudeContrast'] * 100
    cter_data['DefocusAngle'] = 45 - cter_data['DefocusAngle']

    mask = (cter_data['DefocusAngle'] < 0)
    while mask.any():
        cter_data.loc[mask, 'DefocusAngle'] += 180
        mask = (cter_data['DefocusAngle'] < 0)

    mask = (cter_data['DefocusAngle'] >= 180)
    while mask.any():
        cter_data.loc[mask, 'DefocusAngle'] -= 180
        mask = (cter_data['DefocusAngle'] >= 180)

    if 'total_ac' in valid_list:
        cter_data['total_ac'] = cter_data['total_ac'] * 100
    else:
        amp_cont_angle = amplitude_contrast_to_angle(cter_data['AmplitudeContrast'])
        total_phase = amp_cont_angle + cter_data['PhaseShift']
        cter_data['total_ac'] = angle_to_amplitude_contrast(total_phase)

    if 'nyquist' in valid_list:
        cter_data['nyquist'] = 1 / cter_data['nyquist']
    else:
        cter_data['nyquist'] = 1 / (2 * cter_data['PixelSize'])

    if 'resolution_limit_defocus' in valid_list:
        cter_data['resolution_limit_defocus'] = 1 / cter_data['resolution_limit_defocus']
    else:
        cter_data['resolution_limit_defocus'] = cter_data['nyquist']

    if 'resolution_limit_defocus_astig' in valid_list:
        cter_data['resolution_limit_defocus_astig'] = \
            1 / cter_data['resolution_limit_defocus_astig']
    else:
        cter_data['resolution_limit_defocus_astig'] = cter_data['nyquist']

    cter_data['CtfMaxResolution'] = 1 / cter_data['CtfMaxResolution']
    return None


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

    defocus_u = (20000*defocus - 10000*astigmatism) / 2
    defocus_v = 20000*defocus - defocus_u
    return defocus_u, defocus_v


def defocus_u_and_v_to_defocus_defocus_diff(
        defocus_u: pd.Series,
        defocus_v: pd.Series
    ) -> typing.Tuple[pd.Series, pd.Series]:
    """
    Calculate the mean defocus and defocus diff value based on the defocus_u and defocus_v value.

    Arguments:
    defocus_u - Defocus U value
    defocus_v - Defocus V value

    Returns:
    Mean defocus and astigmatism_amplitude
    """
    defocus: pd.Series
    astigmatism_amplitude: pd.Series

    defocus = (defocus_u + defocus_v) / 20000
    astigmatism_amplitude = (-defocus_u + defocus_v) / 10000
    return defocus, astigmatism_amplitude


def amplitude_contrast_to_angle(amp_contrast: pd.Series) -> pd.Series:
    """
    Convert amplitude contrast into an phase shift angle.

    Argument:
    amp_contrast - Value of the amplitude contrast in percent.

    Returns:
    Amplitude contrast value in phase shift in degrees.
    """
    value: pd.Series
    assert (-100 <= amp_contrast).all() and (amp_contrast <= 100).all(), amp_contrast

    value = np.arctan2(amp_contrast, np.sqrt(1e4 - amp_contrast**2))
    mask = (value < 0)
    value.loc[mask] += np.pi
    return np.degrees(value)


def angle_to_amplitude_contrast(angle: pd.Series) -> pd.Series:
    """
    Convert phase shift angle into amplitude contrast percentage.

    Argument:
    angle - Value of the phase shift in degrees

    Returns:
    Value of the amplitude contrast in percent.
    """
    return np.tan(np.radians(angle)) / np.sqrt(1 + np.tan(np.radians(angle))**2) * 100.0
