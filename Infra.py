from subprocess import Popen, PIPE


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
