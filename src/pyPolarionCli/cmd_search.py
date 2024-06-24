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

LOG: logging.Logger = logging.getLogger(__name__)
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


def _parse_nested_search_results(search_result: list[Workitem]) -> list[dict]:
    """Search for work items in a project and return the full work item objects.

    Args:
        project (obj): The project object to search in.
        query (str): The query string to search for work items.

    Returns:
        list[Workitem]: The list of work items.
    """
    output_list: list[dict] = []

    # Iterate over the search results and store them in the output dictionary.
    for workitem in search_result:
        workitem_dict: dict = {}

        # Parse the attributes of the work item recursively.
        # Internal _polarion_item attribute is used to access the work item attributes.
        # pylint: disable=protected-access
        if hasattr(workitem, "_polarion_item"):
            all_items = workitem._polarion_item.__dict__.items()
        else:
            all_items = workitem.__dict__.items()

        for _, value in all_items:
            for key in value:
                _parse_attributes_recursively(
                    workitem_dict, value[key], key)

        # Append the work item dictionary to the results list.
        output_list.append(workitem_dict)

    return output_list


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
    required_subarguments = sub_parser_search.add_argument_group(
        'required arguments')

    required_subarguments.add_argument('-j',
                                       '--project',
                                       type=str,
                                       metavar='<project_id>',
                                       required=True,
                                       help="The ID of the Polarion project to search in.")

    required_subarguments.add_argument('-q',
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

    sub_parser_search.add_argument('--full',
                                   action='store_true',
                                   required=False,
                                   help="Get the full information of the work items. " +
                                   "Can be slow in case of many work items.")

    sub_parser_search.add_argument("--field",
                                   type=str,
                                   action="append",
                                   metavar="<field>",
                                   required=False,
                                   help="The field to search for in the work items. " +
                                   "Can be used multiple times to search for multiple fields.")

    return cmd_dict


def _execute(args, polarion_client: Polarion) -> Ret:
    """ This function serves as entry point for the command 'search'.
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
            LOG.error("%s", ex)
            ret_status = Ret.ERROR_SEARCH_FAILED
        else:
            if args.full is True:
                # Search for work items in the project.
                search_result: list[Workitem] = project.searchWorkitemFullItem(
                    output_dict["query"])

                output_dict["results"] = \
                    _parse_nested_search_results(search_result)
            elif args.field is not None:
                search_result: list[Workitem] = project.searchWorkitem(
                    args.query, field_list=args.field)

                output_dict["results"] = \
                    _parse_nested_search_results(search_result)
            else:
                search_result: list[Workitem] = project.searchWorkitem(
                    args.query)
                for item in search_result:
                    item_dict = vars(item).get("__values__")
                    output_dict["results"].append(item_dict)

            output_dict["number_of_results"] = len(output_dict["results"])

            # Store the search results in a JSON file.
            with open(file_path, 'w', encoding="UTF-8") as file:
                file.write(json.dumps(output_dict, indent=2))

            LOG.info("Search results stored in %s", file_path)
            ret_status = Ret.OK

    return ret_status

################################################################################
# Main
################################################################################
