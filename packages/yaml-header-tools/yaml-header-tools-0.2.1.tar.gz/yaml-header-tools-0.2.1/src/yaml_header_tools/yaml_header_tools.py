#!/usr/bin/env python3
# yaml_header_tools
# Tools to manage yaml header in markdown document

# Copyright (C) 2019-2020 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Authors:
# A. Schlemmer, D. Hornung, T. Fitschen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import yaml
from typing import List

class NoValidHeader(Exception):
    def __init__(self, *args, **kwargs):
        msg = ("Header missing")
        super().__init__(msg, *args, **kwargs)

class MetadataFileMissing(Exception):
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        msg = "Metadata file README.md missing in " + filename
        super().__init__(msg, *args, **kwargs)

class ParseErrorsInHeader(Exception):
    def __init__(self, reason, *args, **kwargs):
        self.reason = reason
        msg = "Invalid header. Reason: {}".format(reason)
        super().__init__(msg, *args, **kwargs)

def get_header_boundaries(textlines: List[str]):
    """
    Retrieves the start end end positions of the yaml header from a list of strings.

    Returns a tuple (start, end) where start is the index of the first line after --- and end
    is the index of the line containing the terminator (--- or ...).
    """
    state = 0
    found_0 = -1
    found_1 = -1
    found_2 = -1
    for i, line in enumerate(textlines):
        if len(line) == 1 and state in {-1, 0}:
            found_0 = i
            state = 0
            continue
        if line.rstrip() == "---" and state == 0:
            found_1 = i+1
            state = 1
            continue
        if (line.rstrip() == "..." or line.rstrip() == "---") and state == 1:
            found_2 = i
            state = 2
            break
        # Else: reset state to -1, unless it is 1 (in this case, leave it
        # untouched
        if state == 1:
            pass
        else:
            state = -1
    if state != 2:
        raise NoValidHeader()
    return found_1, found_2

def find_readme_file(filename_or_dirname: str,
                     create_if_not_exists: bool = False):
    """
    If filename_or_dirname is a directory:
      - Check whether either README.md or readme.md is present in that folder.
      - If the file is found return its fielname.
      - Else raise a MetadataFileMissing exception.
        (Can be controlled using create_if_not_exists.)

    If filename_or_dirname is not a directory just return it.

    If create_if_not_exists is set to True, create the readme file
    instead of throwing an exception.
    """
    filename = filename_or_dirname
    if os.path.isdir(filename):
        filename = os.path.join(filename, "README.md")
        if not os.path.exists(filename):
            filename = filename[:-9]
            filename = os.path.join(filename, "readme.md")
            if not os.path.exists(filename):
                if not create_if_not_exists:
                    raise MetadataFileMissing(filename)
                else:
                    with open(filename, "w") as f:
                        pass
    return filename


def get_header_from_file(filename_or_dirname: str,
                         clean: bool = True, return_main_content: bool = False):
    """
    Open an md file identified by filename_or_dirname and read out the yaml header.

    filename_or_dirname can also be a name of a folder. In this case folder/README.md will be used for
    getting the header. (See find_readme_file for details.)

    If clean is set to True (default) the header is normalized using clean_header.

    if return_main_content is False (default):
    The header is returned as a dictionary.

    if return_main_content is True:
    Additionally the main content is returned as the second entry of the returned tuple.
    """
    filename = find_readme_file(filename_or_dirname)

    with open(filename) as f:
        textlines = f.readlines()

    if not return_main_content:
        return get_header(textlines, clean)
    return get_header(textlines, clean), get_main_content(textlines)


def get_main_content(textlines: List[str]):
    """
    Read out the main content from this markdown file (ignoring the header).

    textlines: list of strings read from the file.

    A list is returned containing only the lines from the main content.
    """

    found_1, found_2 = get_header_boundaries(textlines)

    return textlines[found_2+1:]


def get_header(textlines: List[str], clean: bool = True):
    """
    Read out the yaml header from a list of strings.

    Use the function get_header_from_file to directly load the header from an md file.

    If clean is set to True (default) the header is normalized using clean_header.

    From https://pandoc.org/MANUAL.html:

    A YAML metadata block is a valid YAML object, delimited by a line of three
    hyphens (---) at the top and a line of three hyphens (---) or three dots (...)
    at the bottom. A YAML metadata block may occur anywhere in the document, but if
    it is not at the beginning, it must be preceded by a blank line.
    """

    found_1, found_2 = get_header_boundaries(textlines)

    headerlines = []
    for textline in textlines[found_1:found_2]:
        textline = textline.replace("\t", "  ")  # is that a good idea?
        textline = textline.rstrip()
        headerlines.append(textline)
    try:
        yaml_part = yaml.load("\n".join(headerlines), Loader=yaml.BaseLoader)
    except yaml.scanner.ScannerError as e:
        raise ParseErrorsInHeader(e)
    # except yaml.error.MarkedYAMLError as e:
    #     raise NoValidHeader(filename)
    if type(yaml_part) != dict:
        raise NoValidHeader()
    if clean:
        return clean_header(yaml_part)
    return yaml_part


def save_header_to_file(filename_or_dirname: str, header_data: dict,
                        create_if_not_exists: bool = False):
    """
    Save a header which is a dictionary stored in header_data to the file
    identified by filename_or_dirname.

    The file is expected to already have a valid yaml header.

    filename can also be a folder. In this case folder/README.md will
    be used for getting the header.
    """

    filename = find_readme_file(filename_or_dirname, create_if_not_exists)
    
    with open(filename) as f:
        textlines = f.readlines()

    found_1, found_2 = get_header_boundaries(textlines)

    num_lines = found_2 - found_1
    while num_lines > 0:
        del textlines[num_lines]
        num_lines -= 1

    data = {key: val if len(val) > 1 else val[0] for key, val in header_data.items()}
    textlines.insert(found_1,
                     yaml.dump(data,
                               default_flow_style=False,
                               allow_unicode=True))

    with open(filename, "w") as f:
        f.writelines(textlines)



def add_header_to_file(filename_or_dirname: str, header_dict: dict,
                       create_if_not_exists: bool = False):
    """
    This function is used to add a header to an md file that does not have a header yet.
    """

    filename = find_readme_file(filename_or_dirname, create_if_not_exists)
    
    if os.path.exists(filename):
        with open(filename) as f:
            textlines = f.readlines()
    else:
        textlines = [""]

    localheader = "---\n" + yaml.dump(header_dict,
                                      default_flow_style=False,
                                      allow_unicode=True) + "...\n"

    with open(filename, "w") as f:
        f.write(localheader)
        f.writelines(textlines)


def clean_header(header: dict):
    """
    Normalize a header using the following rules:
    - Fill empty fields (which are either null or None) with empty string
    - If the value to a key is a string, a list with that string as only element is
      returned.

    """
    
    for k, v in header.items():
        if v == "null":
            header[k] = ""
        if v is None:
            header[k] = ""

    for k, v in header.items():
        # Plain string is put into list
        if type(v) == str:
            header[k] = [v]

    return header


def kw_present(header: dict, kw: str):
    """
    Check whether keywords are present in the header.
    """
    return kw in header and header[kw] is not None and len(header[kw]) > 0
