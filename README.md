# C101-TestingInfra

## Description
Tests for C101 course (0512-1820) at TAU.

## Getting Started
* Clone the repository.
* Install `python3`, `pip`, and `pytest`.
* Make sure you have Visual Studio 2019 Community Edition (windows) or gcc (linux) installed.
* Executing tests via terminal (cmd or bash):
```
python3 -m pytest <test_to_execute> --path  <path_to_c_file>
```
* For example:
```
python3 -m pytest test_ex2.py --path /tmp/my_c_file.c
```


### Notes
**Usefull pytest flags:**
* `-s` - Show prints to stdout even if the tests pass.
* `-x` - Stop execution after the first failure (by default, all tests are executed).
* `-k` - Filter tests to execute by keyword.

**This is how I usally execute the tests:**
```
python3 -m pytest c:\Projects\C101-TestingInfra\test_ex3.py --path c:\projects\C101\ex3.py -x
```


### Dependencies
* python3 - Can be installed from: https://www.python.org/downloads/
* pip -Installation instructions: https://pip.pypa.io/en/stable/cli/pip_install/
* pytest - Can be installed from: https://docs.pytest.org/en/7.2.x/getting-started.html#get-started
