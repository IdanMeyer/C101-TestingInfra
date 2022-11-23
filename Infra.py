import pytest
import os
import tempfile
from subprocess import Popen, PIPE, call
from pathlib import Path
import tempfile


class CTestingInfraException(Exception):
    pass

def execute_c_bin(bin_path, input):
    p = Popen([bin_path], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, error = p.communicate(input=str.encode(input))
    if len(error) > 0:
        raise CTestingInfraException(f"C Binary file raised an error: {error}")
    return output

def execute_c_bin_and_parse_result(bin_path, input):
    raw_output = execute_c_bin(bin_path, input)
    split_data = raw_output.decode().split("Result = ")

    if len(split_data) != 2:
        raise CTestingInfraException(f"Invalid output returned: {raw_output}")
    return split_data[-1]

def posix_compile(c_file_path):
    output_path = tempfile.NamedTemporaryFile().name

    print(f"Compiling file: {c_file_path}")
    print(f"Output path: {output_path}")
    command = ["gcc",c_file_path, "-o", output_path, "-lm"]
    result = call(command)
    if result != 0:
        raise CTestingInfraException(f"gcc has failed. Could not compile C file: {c_file_path}")

    return output_path

def windows_compile(c_file_path):
    print(f"Compiling file: {c_file_path}")

    tempdir = tempfile.mkdtemp()

    # TODO: VERY ugly way to handle the path, maybe find a better way
    command = r'call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat" && cd ' +  tempdir + ' && '  + 'cl "'+ c_file_path +'"'
    # TODO: Use call instead of system?
    result = os.system(command)
    if result != 0:
        raise CTestingInfraException(f"gcc has failed. Could not compile C file: {c_file_path}")

    output_path = os.path.join(tempdir, f"{Path(os.path.basename(c_file_path)).stem}.exe")
    return output_path


C_EXEC_PATH = None
def compile_if_needed(path):
    global C_EXEC_PATH

    if C_EXEC_PATH is None:
        if os.name == "posix":
            C_EXEC_PATH = posix_compile(path)
        elif os.name == "nt":
            C_EXEC_PATH = windows_compile(path)
        else:
            raise CTestingInfraException("Could not compile C file. Please compile it manually and input the binary path")

    return C_EXEC_PATH


