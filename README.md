# pyPolarionCli

pyPolarionCli is a command-line tool designed for easy access to Polarion work items, e.g. for metric creation.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/) [![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![CI](https://github.com/NewTec-GmbH/pyPolarionCli/actions/workflows/ci.yml/badge.svg)](https://github.com/NewTec-GmbH/pyPolarionCli/actions/workflows/ci.yml)

* [Installation](#installation)
* [Overview](#overview)
* [Usage](#usage)
* [Commands](#commands)
  * [Search](#search)
* [Examples](#examples)
* [Used Libraries](#used-libraries)
* [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
* [License](#license)
* [Contribution](#contribution)

## Installation

```cmd
git clone https://github.com/NewTec-GmbH/pyPolarionCli.git
cd pyPolarionCli
pip install .
```

## Overview

![overview](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/NewTec-GmbH/pyPolarionCli/main/design/UML/context.puml)

## Usage

Show help information:

```cmd
pyPolarionCli --help
```

## Commands

### Search

Search for Work items on the Polarion Server.
The query must be in the Polarion format.

Example:

```cmd
pyPolarionCli --user my_username --password my_password --server my_server search --project my_project --query "author.id:myname"

```

Try the search command by executing the [batch file](./examples/search/search.bat).

## Examples

Check out the all the [Examples](./examples) on how to use the pyPolarionCli tool.

## Used Libraries

Used 3rd party libraries which are not part of the standard Python package:

* [polarion](https://pypi.org/project/polarion/) - Python library for interacting with Polarion - MIT License
* [toml](https://github.com/uiri/toml) - Parsing [TOML](https://en.wikipedia.org/wiki/TOML) - MIT License

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create an [issue](https://github.com/NewTec-GmbH/pyPolarionCli/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/pyPolarionCli/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
