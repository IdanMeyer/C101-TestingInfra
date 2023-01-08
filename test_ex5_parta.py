import os
import sys
import pytest
import math
import random
import re

import Infra


compiled_path = None
@pytest.fixture(scope='session', autouse=True)
def compile(request):
    c_file_path = request.config.option.path
    print(request.config.option.path)
    global compiled_path
    compiled_path = Infra.compile_if_needed(c_file_path)


def execute_ex5_test(original_list, expected_output_list):
    # input_string = f"{a}{os.linesep}{b}{os.linesep}{c}{os.linesep}{os.linesep}"
    input_string = f""
    for i in original_list:
        input_string += f"{i}{os.linesep}"
    result = Infra.execute_c_bin(compiled_path, input_string).decode()

    output_list = result.split('Modified Linked list:')[1].strip().split()
    output_list = [int(x) for x in output_list]

    assert len(output_list) == len(expected_output_list)
    assert output_list == expected_output_list


class TestQuestion1(object):

    def test_sanity(self):
        execute_ex5_test([0, 1, 8, 667, 56, 250, 16, -1], [16, 250, 56, 8,0, 667, 1])
        execute_ex5_test([1000, 1, 8,667,56,250,13,-5], [250, 56, 8,1000, 13, 667, 1])
