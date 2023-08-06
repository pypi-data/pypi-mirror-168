# Conflook

A command line utiltiy for inspecting hard-to-read project config files such as json, yaml, and toml.

## Usage

```
Usage: conflook [OPTIONS] FILE [KEYPATH]

  Show summarised structure or value at keypath.

Options:
  -v, --version        Show the version and exit.
  -h, --help           Show this message and exit.
  -l, --limit INTEGER  Default 10. Truncate output if more than `limit` lines.
                       If 0, there is no limit.
```

Keypath is a dot separated list of keys or indicies. For example, `database.ports.2` would access the `database` table, then the `ports` array within that, then the 3rd item (at index 2) within that array. A consequence of this notation is that not all possible keys can be addressed.

If the value at the end of a valid keypath is a map-like object then it is shown as a list of keys followed by their type followed by a preview of their contents.

For example,

```
database, Table(4)
server         String(11) 192.168.1.1
ports          Array(3)   [8001, 8001, 8002]
connection_max Integer    5000
enabled        bool       True
```

A content preview attempts to be close to the real text content in the configuration file. For example, a YAML `!!binary` entry will not be decoded. Control sequences (eg newlines) in strings will be escaped.

Note that if no matching key is found in a keypath then conflook will show

- The shortest key for which the given key is a prefix, or
- The closest matching key as determined by difflib

For example,

```
conflook eg.toml data.prots
```

Gives

```
database.ports, Array(3)
[8001, 8001, 8002]
```

## Install

[Avaliable on PyPI](https://pypi.org/project/conflook/).

- Install with PIP.

  ```
  pip install conflook
  ```

  Run from command line

  ```
  conflook --help
  ```

- OR, Add as development dependancy to PDM project.

  ```
  pdm add --dev conflook
  ```

  Run from `pdm`

  ```
  pdm run conflook --help
  ```

## Develop

1. Download this repository `git clone ...`.

2. [Install PDM](https://pdm.fming.dev/#installation).
   Use PDM to install python dependancies with `pdm sync`.

   PDM will keep the versions of 3rd party libraries consistent with `pdm.lock`. The 3rd party libraries which this project depend on are listed in `pyproject.toml` along with other project settings used by the [PyPI](https://pypi.org) and exposing a command when installed.

3. [Enable pre-commit](https://pre-commit.com/#install).
   Will run automatic checks for each `git commit`, as described in `.pre-commit-config.yaml`. Might need to run `pdm run pre-commit install` to setup. [Pylint](https://pylint.org) will check for the things specified in `pylintrc.toml`. Sometimes these checks can be ignored with a `# pylint: disable=` comment if they are too pedantic.

PDM should install an editable package. Make sure to put `pdm run` before any commands to make sure the correct Python interpreter is being used and the projects dependancies are avaliable. For example, `pdm run conflook ...` will run this utility, `pdm run pre-commit run` will manually run pre-commit checks, and `pdm run python` will start an interactive python session.

The folder `eg/` contains example files.
