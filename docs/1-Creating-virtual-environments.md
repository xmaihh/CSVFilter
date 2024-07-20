# virtualenv — Creation of virtual environments

[virtualenv](https://virtualenv.pypa.io/en/latest/) is a tool to create isolated Python environments.

# User Guide

Create the environment (creates a folder in your current directory)

```shell
virtualenv env_name
```

In Linux or Mac, activate the new python environment

```shell
source env_name/bin/activate
```

Or in Windows

```shell
.\env_name\Scripts\activate
```

Confirm that the env is successfully selected

```shell
which python3
```

# Quickstart

> ⚠️ CSVFilter works with **Python 3.7+**. To check your Python version, run [`python --version`](https://docs.python.org/3/using/cmdline.html#cmdoption-version).
>
> If you have both Python 2 and Python 3 installed, you may need to use `python3` instead of `python`. This is becoming less common as [Python 2 is sunsetting](https://www.python.org/doc/sunset-python-2/).

The source command might vary by shell - e.g. on Bash it’s `source` (or `.`):

```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate
python main.py
```

The scripts also provision a `deactivate` command that will allow you to undo the operation:

```shell
deactivate
```

**Note**: all of the remaining example commands assume you've activated your project's virtual environment.