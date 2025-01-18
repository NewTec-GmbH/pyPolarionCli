# pyPolarionCli

pyPolarionCli is a command-line tool designed for easy access to Polarion work items, e.g. for metric creation.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/) [![Repo Status](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![CI](https://github.com/NewTec-GmbH/pyPolarionCli/actions/workflows/ci.yml/badge.svg)](https://github.com/NewTec-GmbH/pyPolarionCli/actions/workflows/ci.yml)

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Flags](#flags)
  - [Login options](#login-options)
- [Commands](#commands)
- [Examples](#examples)
- [Compile into an executable](#compile-into-an-executable)
- [Used Libraries](#used-libraries)
- [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
- [License](#license)
- [Contribution](#contribution)

## Overview

![overview](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/NewTec-GmbH/pyPolarionCli/main/doc/uml/context.puml)

More information on the deployment and architecture can be found in the [doc](./doc/README.md) folder.

## Installation

```cmd
git clone https://github.com/NewTec-GmbH/pyPolarionCli.git
cd pyPolarionCli
pip install .
```

## Usage

```cmd
pyPolarionCli [-h] -u <user> -p <password> -s <server_url> [--version] [-v] {command} {command_options}
```

### Flags

| Flag           | Description                                                                                     |
| :------------: | ----------------------------------------------------------------------------------------------- |
| --verbose , -v | Print full command details before executing the command. Enables logs of type INFO and WARNING. |
| --version      | Show  version information.                                                                      |
| --help , -h    | Show the help message and exit.                                                                 |

### Login options

To connect to the Polarion server, provide all credentials via Command Line arguments:
    - `--server <server URL>` is required.
    - ID using `--user <user>` and `--password <password>`

## Commands

| Command                                     | Description                                         |
| :-----------------------------------------: | --------------------------------------------------- |
|[search](./doc/commands/search.md)           | Search for Polarion work items.                     |

## Examples

Check out the all the [Examples](./examples) on how to use the pyPolarionCli tool.

## Compile into an executable

It is possible to create an executable file that contains the tool and all its dependencies. "PyInstaller" is used for this.
Just run the following command on the root of the folder:

```cmd
pyinstaller --noconfirm --onefile --console --name "pyPolarionCli" --add-data "./pyproject.toml;."  "./src/pyPolarionCli/__main__.py"
```

## Used Libraries

Used 3rd party libraries which are not part of the standard Python package:

- [polarion](https://pypi.org/project/polarion/) - Python library for interacting with Polarion - MIT License
- [toml](https://github.com/uiri/toml) - Parsing [TOML](https://en.wikipedia.org/wiki/TOML) - MIT License

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create an [issue](https://github.com/NewTec-GmbH/pyPolarionCli/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/pyPolarionCli/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
