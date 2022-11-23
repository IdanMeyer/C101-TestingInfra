import Infra
import os

os.linesep
C_EXEC_PATH = "/tmp/exec"

def execute_ex2_test(question_number, question_input, expected_output):
    input_string = f"{question_number}{os.linesep}{question_input}{os.linesep}"
    result = Infra.execute_c_bin_and_parse_result(C_EXEC_PATH, input_string)
    assert result == expected_output


def test_always_passes():
    # out = Infra.execute_c_bin(C_EXEC_PATH, f"1{os.linesep}10{os.linesep}")
    execute_ex2_test(1, 10, "1010")
