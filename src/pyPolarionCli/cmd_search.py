"""Search command module of the pyPolarionCli"""

# BSD 3-Clause License
#
# Copyright (c) 2024, NewTec GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICU5LAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################################################################
# Imports
################################################################################

import json
import argparse
import logging
from datetime import date, datetime
from polarion.polarion import Polarion
from polarion.project import Project
from polarion.workitem import Workitem
from pyPolarionCli.ret import Ret

################################################################################
# Variables
################################################################################

_CMD_NAME = "search"
_OUTPUT_FILE_NAME = "search_results.json"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def _handle_object_with_dict(obj_with_dict: object) -> dict:
    """
    Handle an object with a __dict__ attribute.

    Args:
        obj_with_dict (obj): The object to handle.

    Returns:
        dict: The dictionary representation of the object.
    """
    parsed_dict: dict = {}
    for _, subvalue in obj_with_dict.__dict__.items():
        for subkey in subvalue:
            _parse_attributes_recursively(
                parsed_dict,
                subvalue[subkey],
                subkey)
    return parsed_dict


def _parse_attributes_recursively(output_dict: dict, value: object, key: str) -> None:
    """
    Parse the attributes of Python objects recursively and store them in a dictionary.

    Args:
        output_dict (dict): The dictionary to store the parsed attributes.
        value (obj): The value to parse.
        key (str): The key of the value in the dictionary.

    Returns:
        None
    """
    attribute_value = None

    # Check if the value is a datetime or date object
    if isinstance(value, (datetime, date)):
        attribute_value = value.isoformat()

    # Check if the value is a list
    elif isinstance(value, list):
        sublist: list = []
        for element in value:
            # Check if the element is an object with a __dict__ attribute
            if hasattr(element, "__dict__"):
                sublist.append(_handle_object_with_dict(element))

            # Check if the element is a list
            elif isinstance(element, list):
                raise RuntimeWarning("List in List")

            # element is a simple value
            else:
                sublist.append(element)

        # Store the list in the attribute value
        attribute_value = sublist

    # Check if the value is an object with a __dict__ attribute
    elif hasattr(value, "__dict__"):
        attribute_value = _handle_object_with_dict(value)

    # value is a simple value
    else:
        attribute_value = value

    # Store the attribute value in the output dictionary
    output_dict[key] = attribute_value


def register(subparser) -> dict:
    """ Register subparser commands for the login module.

    Args:
        subparser (obj):   the command subparser provided via __main__.py

    Returns:
        obj:    the command parser of this module
    """
    cmd_dict: dict = {
        "name": _CMD_NAME,
        "handler": _execute
    }

    sub_parser_search: argparse.ArgumentParser = \
        subparser.add_parser(_CMD_NAME,
                             help="Search for Polarion work items.")

    sub_parser_search.add_argument('-p',
                                   '--project',
                                   type=str,
                                   metavar='<project_id>',
                                   required=True,
                                   help="The ID of the Polarion project to search in.")

    sub_parser_search.add_argument('-q',
                                   '--query',
                                   type=str,
                                   metavar='<query>',
                                   required=True,
                                   help="The query string to search for work items.")

    sub_parser_search.add_argument('-o',
                                   '--output',
                                   type=str,
                                   metavar='<output_folder>',
                                   required=False,
                                   help="The path to output folder to store the search results.")

    return cmd_dict


def _execute(args, polarion_client: Polarion) -> Ret:
    """ This function servers as entry point for the command 'search'.
        It will be stored as callback for this module's subparser command.

    Args: 
        args (obj): The command line arguments.
        polarion_client (obj): The Polarion client object.

    Returns:
        bool: The status of the command execution.
    """
    ret_status: Ret = Ret.ERROR_INVALID_ARGUMENTS

    if ("" != args.project) and ("" != args.query) and (None is not polarion_client):
        output_folder: str = "."
        output_dict: dict = {
            "project": args.project,
            "query": args.query,
            "number_of_results": 0,
            "results": [],
        }

        if args.output is not None:
            output_folder = args.output

        file_path: str = f"{output_folder}/{output_dict['project']}_{_OUTPUT_FILE_NAME}"

        try:
            # Get the project object from the Polarion client.
            project: Project = polarion_client.getProject(
                output_dict['project'])
        # Exception of type Exception is raised when the project does not exist.
        except Exception as ex:  # pylint: disable=broad-except
            logging.error("%s", ex)
            ret_status = Ret.ERROR_SEARCH_FAILED
        else:
            # Search for work items in the project.
            search_result: list[Workitem] = project.searchWorkitemFullItem(
                output_dict['query'])

            output_dict["number_of_results"] = len(search_result)

            # Iterate over the search results and store them in the output dictionary.
            for workitem in search_result:
                workitem_dict: dict = {}

                # Parse the attributes of the work item recursively.
                # Internal _polarion_item attribute is used to access the work item attributes.
                # pylint: disable=protected-access
                for _, value in workitem._polarion_item.__dict__.items():
                    for key in value:
                        _parse_attributes_recursively(
                            workitem_dict, value[key], key)

                # Append the work item dictionary to the results list.
                output_dict["results"].append(workitem_dict)

            # Store the search results in a JSON file.
            with open(file_path, 'w', encoding="UTF-8") as file:
                file.write(json.dumps(output_dict, indent=2))

            logging.info("Search results stored in %s", file_path)
            ret_status = Ret.OK

    return ret_status

################################################################################
# Main
################################################################################
