import pytest
import os
import tempfile
from subprocess import Popen, PIPE, call


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
        raise CTestingInfraException(f"gcc has failed. Could not compile C file")

    return output_path



C_EXEC_PATH = None
def compile_if_needed(path):
    global C_EXEC_PATH
    # c_file_path = "/home/idan/Projects/C101/C101/EX2/ex2_313333775.c"

    if C_EXEC_PATH is None:
        if os.name == "posix":
            C_EXEC_PATH = posix_compile(path)
        else:
            raise CTestingInfraException("Could not compile C file. Please compile it manually and input the binary path")

        return C_EXEC_PATH

    return C_EXEC_PATH

