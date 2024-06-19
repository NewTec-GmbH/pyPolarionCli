"""The main module with the program entry point."""

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

import sys
import argparse
import logging
from polarion.polarion import Polarion

from .version import __version__, __author__, __email__, __repository__, __license__
from .ret import Ret


################################################################################
# Variables
################################################################################

# Add command modules here
_CMD_MODULES = [
]

PROG_NAME = "pyPolarionCli"
PROG_DESC = "CLI tool for easy access to Polarion work items, e.g. for metric creation."
PROG_COPYRIGHT = f"Copyright (c) 2024 NewTec GmbH - {__license__}"
PROG_GITHUB = f"Find the project on GitHub: {__repository__}"
PROG_EPILOG = f"{PROG_COPYRIGHT} - {PROG_GITHUB}"

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

    parser.add_argument('-u',
                        '--user',
                        type=str,
                        metavar='<user>',
                        help="The user to authenticate with the Polarion server")

    parser.add_argument('-p',
                        '--password',
                        type=str,
                        metavar='<password>',
                        help="The password to authenticate with the Polarion server")

    parser.add_argument('-s',
                        '--server',
                        type=str,
                        metavar='<server URL>',
                        help="The Polarion server URL to connect to.")

    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s " + __version__)

    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Print full command details before executing the command.\
                            Enables logs of type INFO and WARNING.")

    # to do: Register subparsers once the command files are generated.

    return parser


def main() -> int:
    """ The program entry point function.

    Returns:
        int: System exit status.
    """
    ret_status = Ret.OK

    # Parse the command line arguments.
    parser = add_parser()
    args = parser.parse_args()

    if args is None:
        ret_status = Ret.ERROR_ARGPARSE
    else:
        # If the verbose flag is set, change the default logging level.
        if args.verbose:
            logging.basicConfig(level=logging.INFO)

        logging.info("Program arguments: ")

        for arg in vars(args):
            logging.info("* %s = %s", arg, vars(args)[arg])

        # Create a Polarion client which communicates to the Polarion server.
        # A broad exception has to be caught since the specific Exception Type can't be accessed.
        try:
            # to do: remove the "pylint: disable" once the client is used.
            # pylint: disable=unused-variable
            client = Polarion(polarion_url=args.server,
                              user=args.user,
                              password=args.password,
                              verify_certificate=False,
                              static_service_list=True)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error(e)
            ret_status = Ret.ERROR_LOGIN

        if Ret.OK == ret_status:
            pass
            # to do: Call the respective Function and pass the
            # Polarion Client once the Commands are implemented

    return ret_status

################################################################################
# Main
################################################################################


if __name__ == "__main__":
    sys.exit(main())
