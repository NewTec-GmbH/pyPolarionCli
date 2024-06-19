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
from polarion.polarion import Polarion
from polarion.workitem import Workitem
from .ret import Ret

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


def register(subparser) -> dict:
    """ Register subparser commands for the login module.

    Args:
        subparser (obj):   the command subparser provided via __main__.py

    Returns:
        obj:    the command parser of this module
    """
    cmd_dict = {
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
        It will be stored as callback for this modules subparser command.

    Args: 
        args (obj): The command line arguments.
        polarion_client (obj): The Polarion client object.

    Returns:
        bool: The status of the command execution.
    """
    ret_status = Ret.ERROR_INVALID_ARGUMENTS

    if ("" != args.project) and ("" != args.query) and (None is not polarion_client):
        project_id: str = args.project
        query: str = args.query
        output_folder = "."
        output_dict: dict = {
            "project": project_id,
            "query": query,
            "number_of_results": 0,
            "results": [],
        }

        if args.output is not None:
            output_folder = args.output

        file_path = f"{output_folder}/{project_id}_{_OUTPUT_FILE_NAME}"

        search_result: list[Workitem] = polarion_client.getProject(
            project_id).searchWorkitem(query)

        output_dict["number_of_results"] = len(search_result)

        for item in search_result:
            item_dict = vars(item).get("__values__")
            output_dict["results"].append(item_dict)

        with open(file_path, 'w', encoding="UTF-8") as file:
            file.write(json.dumps(output_dict, indent=2))

        logging.info("Search results stored in %s", file_path)
        ret_status = Ret.OK

    return ret_status

################################################################################
# Main
################################################################################
