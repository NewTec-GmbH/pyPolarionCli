"""The main module with the program entry point."""

# BSD 3-Clause License
#
# Copyright (c) 2024 - 2025, NewTec GmbH
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

import sys
import argparse
import logging
from polarion.polarion import Polarion

from pyPolarionCli.version import __version__, __author__, __email__, __repository__, __license__
from pyPolarionCli.ret import Ret
from pyPolarionCli.cmd_search import register as cmd_search_register


################################################################################
# Variables
################################################################################

# Register a command here!
_COMMAND_REG_LIST = [
    cmd_search_register
]

PROG_NAME = "pyPolarionCli"
PROG_DESC = "CLI tool for easy access to Polarion work items, e.g. for metric creation."
PROG_COPYRIGHT = f"Copyright (c) 2024 NewTec GmbH - {__license__}"
PROG_GITHUB = f"Find the project on GitHub: {__repository__}"
PROG_EPILOG = f"{PROG_COPYRIGHT} - {PROG_GITHUB}"

LOG: logging.Logger = logging.getLogger(__name__)

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def add_parser() -> argparse.ArgumentParser:
    """ Add parser for command line arguments and
        set the execute function of each 
        cmd module as callback for the subparser command.
        Return the parser after all the modules have been registered
        and added their subparsers.


    Returns:
        argparse.ArgumentParser:  The parser object for commandline arguments.
    """
    parser = argparse.ArgumentParser(prog=PROG_NAME,
                                     description=PROG_DESC,
                                     epilog=PROG_EPILOG)

    required_arguments = parser.add_argument_group('required arguments')

    required_arguments.add_argument('-u',
                                    '--user',
                                    type=str,
                                    metavar='<user>',
                                    required=True,
                                    help="The user to authenticate with the Polarion server.")

    required_arguments.add_argument('-p',
                                    '--password',
                                    type=str,
                                    metavar='<password>',
                                    required=False,
                                    help="The password to authenticate with the Polarion server.\
                                    Is ignored if a token is defined using -t option.")

    required_arguments.add_argument('-t',
                                    '--token',
                                    type=str,
                                    metavar='<token>',
                                    required=False,
                                    help="The token to authenticate with the Polarion server.")

    required_arguments.add_argument('-s',
                                    '--server',
                                    type=str,
                                    metavar='<server_url>',
                                    required=True,
                                    help="The Polarion server URL to connect to.")

    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s " + __version__)

    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Print full command details before executing the command.\
                            Enables logs of type INFO and WARNING.")

    return parser


def main() -> Ret:
    """ The program entry point function.

    Returns:
        int: System exit status.
    """
    ret_status = Ret.OK
    commands = []

    # Create the main parser and add the subparsers.
    parser = add_parser()
    subparser = parser.add_subparsers(required=True, dest="cmd")

    # Register all commands.
    for cmd_register in _COMMAND_REG_LIST:
        cmd_par_dict = cmd_register(subparser)
        commands.append(cmd_par_dict)

    # Parse the command line arguments.
    args = parser.parse_args()

    # Check if the command line arguments are valid.
    if args is None:
        ret_status = Ret.ERROR_ARGPARSE
        parser.print_help()
    elif (args.password is None) and (args.token is None):
        ret_status = Ret.ERROR_INVALID_ARGUMENTS
        LOG.error("Missing password or token!")
    else:
        # If the verbose flag is set, change the default logging level.
        if args.verbose:
            logging.basicConfig(level=logging.INFO)
            LOG.info("Program arguments: ")
            for arg in vars(args):
                LOG.info("* %s = %s", arg, vars(args)[arg])

        # Create a Polarion client which communicates to the Polarion server.
        # A broad exception has to be caught since the specific Exception Type can't be accessed.
        try:
            client = Polarion(polarion_url=args.server,
                              user=args.user,
                              password=args.password,
                              token=args.token,
                              verify_certificate=False,
                              static_service_list=True)
        except Exception as e:  # pylint: disable=broad-exception-caught
            LOG.error(e)
            ret_status = Ret.ERROR_LOGIN

        if Ret.OK == ret_status:
            handler = None

            # Find the command handler.
            for command in commands:
                if command["name"] == args.cmd:
                    handler = command["handler"]
                    break

            # Execute the command.
            if handler is not None:
                ret_status = handler(args, client)
            else:
                LOG.error("Command '%s' not found!", args.cmd)
                ret_status = Ret.ERROR_INVALID_ARGUMENTS

    return ret_status

################################################################################
# Main
################################################################################


if __name__ == "__main__":
    sys.exit(main())
