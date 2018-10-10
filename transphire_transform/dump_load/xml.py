"""
    TranSPHIRE is supposed to help with the cryo-EM data collection
    Copyright (C) 2017 Markus Stabrin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import typing
import re
import xml.etree.ElementTree as et

import pandas as pd # type: ignore

from . import util


def get_key_without_prefix(key: str) -> str:
    """
    Return the key of the XML entry by removing trailing and leading whitespaces
    and underscores.

    Arguments:
    key - XML key

    Returns:
    Key without trailing and leading whitespace and underscore
    """
    return_key: str
    xml_key_match: typing.Optional[typing.Match[str]]

    xml_key_match = re.match(r'.*{.*}(.*)', key)
    if xml_key_match is None:
        return_key = key
    else:
        return_key = xml_key_match.group(1)
    return return_key.strip().strip('_')


def get_all_key_value(
        node: et.Element,
        key: str,
        search_keys: typing.List[str],
        data_dict: typing.Dict[str, str]
    ) -> None:
    """
    Return all the entries that are mapped to an Key:Value pair inside the XML file.
    Case:

    <key>entry_dict</key>
    <search_key>entry_value</search_key>

    Arguments:
    node - Node in the xml tree
    key - Name of the key entry
    search_keys - Name of the value entry
    data_dict - Dictionary that contains the XML information

    Returns:
    None
    """
    findall_key: typing.List[et.Element]
    sub_value_keys_dict: typing.Dict[
        str,
        typing.Callable[[et.Element, typing.Dict[str, str]], None]
        ]
    child_values: typing.List[et.Element]
    dose_frac_key: str
    number_of_frac_key: str

    dose_frac_key = '{http://schemas.datacontract.org/2004/07/Fei.Applications.Common.Omp.Interface}DoseFractions' # pylint: disable=line-too-long
    number_of_frac_key = '{http://schemas.datacontract.org/2004/07/Fei.Applications.Common.Omp.Interface}NumberOffractions' # pylint: disable=line-too-long
    sub_value_keys_dict = {
        dose_frac_key: dose_frac_nested_values,
        number_of_frac_key: number_frac_nested_values,
        }

    findall_key = node.findall(key)
    if findall_key:
        child_values = fill_key_value_dict(
            findall_key=findall_key,
            findall_value=node.findall(search_keys[0]),
            data_dict=data_dict
            )

        for child in child_values:
            for grand_child in child:
                try:
                    sub_value_keys_dict[grand_child.tag](grand_child, data_dict)
                except KeyError:
                    pass

    else:
        pass

    return None


def fill_key_value_dict(
        findall_key: typing.List[et.Element],
        findall_value: typing.List[et.Element],
        data_dict: typing.Dict[str, str],
    ) -> typing.List[et.Element]:
    """
    Fill the dictionary with key value pairs.

    Arguments:
    findall_key - XML element nodes containing the Keys
    findall_value - XML element nodes containing the Values
    data_dict - Dictionary storing the information

    Returns:
    List of nested value nodes
    """
    child_values: typing.List[et.Element]

    assert len(findall_key) == len(findall_value)
    child_values = []
    for entry_key, entry_value in zip(findall_key, findall_value):
        if entry_value.text:
            assert entry_key.text is not None
            util.add_to_dict(data_dict, entry_key.text, entry_value.text)
        else:
            child_values.append(entry_value)

    return child_values


def dose_frac_nested_values(node: et.Element, data_dict: typing.Dict[str, str]) -> None:
    """
    Return the number of fractions for an Falcon xml file

    Arguments:
    node - Dictionary storing the information
    data_dict - Dictionary containin the extracted xml data

    Returns:
    None
    """
    start: typing.Optional[str]
    end: typing.Optional[str]

    start = None
    end = None
    for grand_child in node.iter():
        if 'StartFrameNumber' in grand_child.tag:
            start = grand_child.text
        if 'EndFrameNumber' in grand_child.tag:
            end = grand_child.text
        if start and end:
            break

    if start is not None and end is not None:
        util.add_to_dict(data_dict, 'NumberOffractions', str(len(node)))
        util.add_to_dict(
            data_dict,
            'FramesPerFraction',
            str(int(end.strip()) - int(start.strip()) + 1)
            )
    return None


def number_frac_nested_values(node: et.Element, data_dict: typing.Dict[str, str]) -> None:
    """
    Return the number of fractions for an K2 xml file

    Arguments:
    node - Dictionary storing the information
    data_dict - Dictionary containin the extracted xml data

    Returns:
    None
    """
    assert node.text is not None
    util.add_to_dict(data_dict, 'NumberOffractions', str(int(node.text.strip())))
    util.add_to_dict(data_dict, 'FramesPerFraction', '1')
    return None


def get_level_0_xml(
        node: et.Element,
        key: str,
        search_keys: typing.List[str],
        data_dict: typing.Dict[str, str]
    ) -> None:
    """
    Return the key/value pair for the xml case

    <key>Value</key>.

    Arguments:
    node - Node in the xml tree
    key - Name of the key entry
    data_dict - Dictionary that contains the XML information
    **kwargs - Additional kwargs, needed to be here to be consistent with the other functions

    Returns:
    None
    """
    assert not search_keys
    if key == node.tag:
        dict_key = get_key_without_prefix(node.tag)
        if node.text:
            util.add_to_dict(data_dict, dict_key, node.text)
    else:
        pass

    return None


def get_level_1_xml(
        node: et.Element,
        key: str,
        search_keys: typing.List[str],
        data_dict: typing.Dict[str, str]
    ) -> None:
    """
    Return the key/value pair for the xml case

    <key>
    <subkey>value</subkey>
    </key>

    Arguments:
    node - Node in the xml tree
    key - Name of the key entry
    data_dict - Dictionary that contains the XML information
    **kwargs - Additional kwargs, needed to be here to be consistent with the other functions

    Returns:
    None
    """
    search_keys_no_prefix: typing.List[str]
    key_1: str
    key_2: str
    combined_key: str

    search_keys_no_prefix = [get_key_without_prefix(search_key) for search_key in search_keys]
    if key == node.tag:
        key_1 = get_key_without_prefix(key)

        for child in node:
            key_2 = get_key_without_prefix(child.tag)
            combined_key = '_'.join([key_1, key_2])

            for key_check in search_keys_no_prefix:
                if key_check == key_2:
                    assert child.text is not None
                    util.add_to_dict(data_dict, combined_key, child.text)
    else:
        pass

    return None


def get_level_3_xml(
        node: et.Element,
        key: str,
        search_keys: typing.List[str],
        data_dict: typing.Dict[str, str]
    ) -> None:
    """
    Return the key/value pair for the xml case

    <key>
    <subkey_1>
    <subkey_2>value</subkey_2>
    </subkey_1>
    </key>

    Arguments:
    node - Node in the xml tree
    key - Name of the key entry
    data_dict - Dictionary that contains the XML information
    **kwargs - Additional kwargs, needed to be here to be consistent with the other functions

    Returns:
    None
    """
    search_keys_no_prefix: typing.List[str]
    key_1: str
    key_2: str
    combined_key: str
    test_tag: str
    list_key: typing.List[str]
    list_child: typing.List[et.Element]

    if key == node.tag:
        search_keys_no_prefix = [get_key_without_prefix(search_key) for search_key in search_keys]
        list_key = []
        list_child = []

        for child in node:
            key_1 = get_key_without_prefix(child.tag)

            for grand_child in child:
                key_2 = get_key_without_prefix(grand_child.tag)
                combined_key = '_'.join([key_1, key_2])
                list_key.append(combined_key)
                list_child.append(grand_child)

        assert len(list_key) == len(list_child)
        for combined_key, child in zip(list_key, list_child):
            for grand_child in child:
                test_tag = get_key_without_prefix(grand_child.tag)

                for key_check in search_keys_no_prefix:
                    if key_check == test_tag:
                        assert grand_child.text is not None
                        util.add_to_dict(data_dict, combined_key, grand_child.text)
    else:
        pass

    return None


def recursive_node(
        node: et.Element,
        data_dict: typing.Dict[str, str],
        level_dict: typing.Dict[str, typing.Dict[str, typing.List[str]]],
        level_func_dict: typing.Dict[
            str,
            typing.Callable[
                [et.Element, str, typing.List[str], typing.Dict[str, str]],
                None
                ]
            ]
    ) -> None:
    """
    Find all xml information recursively.

    Arguments:
    node - Current node to search
    data_dict - Dictionary containing the extracted data
    level_dict - Dinctionary containing the searched keys for each level
    level_func_dict - Dictionary containing the different level functions

    Returns:
    None - Dictionary will be modified inplace
    """

    for level_key, level_value in level_dict.items():
        for key, value in level_value.items():
            level_func_dict[level_key](
                node,
                key,
                value,
                data_dict,
                )

    for child in node:
        recursive_node(
            node=child,
            data_dict=data_dict,
            level_dict=level_dict,
            level_func_dict=level_func_dict
            )

    return None


def load_xml(
        file_name: str,
        level_dict: typing.Dict[str, typing.Dict[str, typing.List[str]]]
    ) -> pd.DataFrame:
    """
    Extract the xml information from the file.

    Arguments:
    file_name - Path to the xml file
    level_dict - Dictionary containin the keys to extract

    Returns:
    Pandas data frame containing the information
    """
    level_func_dict: typing.Dict[
        str,
        typing.Callable[
            [et.Element, str, typing.List[str], typing.Dict[str, str]],
            None
            ]
        ]
    tree: et.ElementTree
    root: et.Element
    data_dict: typing.Dict[str, str]

    level_func_dict = {
        'key_value': get_all_key_value,
        'level 0': get_level_0_xml,
        'level 1': get_level_1_xml,
        'level 3': get_level_3_xml,
        }

    tree = et.parse(file_name)
    root = tree.getroot()
    data_dict = {}
    recursive_node(
        node=root,
        data_dict=data_dict,
        level_dict=level_dict,
        level_func_dict=level_func_dict
        )


    return pd.DataFrame(data_dict, index=[0])
