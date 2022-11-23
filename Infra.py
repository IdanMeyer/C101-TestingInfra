from subprocess import Popen, PIPE


def execute_c_bin(bin_path, input):
    p = Popen([bin_path], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, error = p.communicate(input=str.encode(input))
    return output

def execute_c_bin_and_parse_result(bin_path, input):
    raw_output = execute_c_bin(bin_path, input)
    return raw_output.decode().split("Result = ")[-1]
