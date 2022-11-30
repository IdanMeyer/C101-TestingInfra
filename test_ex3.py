import os
import sys
import pytest
import math
import random

import Infra


compiled_path = None
@pytest.fixture(scope='session', autouse=True)
def compile(request):
    c_file_path = request.config.option.path
    print(request.config.option.path)
    global compiled_path
    compiled_path = Infra.compile_if_needed(c_file_path)


def execute_ex3_test(question_number, question_input, expected_output):
    input_string = f"{question_number}{os.linesep}{question_input}{os.linesep}"
    result = Infra.execute_c_bin_and_parse_result(compiled_path, input_string)
    assert result == expected_output


class TestQuestion1(object):
    QUESTION_NUMBER = 1

    def test_sanity(self):
        execute_ex3_test(self.QUESTION_NUMBER, "1,-2,1,1,-2,1", "2")

    def test_examples(self):
        execute_ex3_test(self.QUESTION_NUMBER, "1,-2,1,1,-2,1", "2")
        execute_ex3_test(self.QUESTION_NUMBER, "-2,-3,4,-1,-2,1,5,-3", "5")

    def test_only_negative_numbers(self):
        execute_ex3_test(self.QUESTION_NUMBER, "-1", "1")
        execute_ex3_test(self.QUESTION_NUMBER, "-1,-2,-3", "1")
        execute_ex3_test(self.QUESTION_NUMBER, "-30,-70,-85", "1")

    def test_zero(self):
        execute_ex3_test(self.QUESTION_NUMBER, "0", "1")
        execute_ex3_test(self.QUESTION_NUMBER, "0,0", "1")
        execute_ex3_test(self.QUESTION_NUMBER, "0,0,0", "1")

    def get_max_sublist(self, lst):
        all_options = [lst[i: j] for i in range(len(lst)) for j in range(i + 1, len(lst) + 1)]
        max_sum = 0
        max_length = 1
        for option in all_options:
            if sum(option) > max_sum:
                max_sum = sum(option)
                max_length = len(option)
        return max_length

    @pytest.mark.parametrize('iter_number',range(1, 100))
    @pytest.mark.parametrize('number_of_items',range(1, 10))
    def test_automated(self, iter_number, number_of_items):
        lst = [random.randint(-100, +100) for x in range(number_of_items)]
        print(f"input number: {lst}")
        expected_output = self.get_max_sublist(lst)
        print(f"expected_output: {expected_output}")
        execute_ex3_test(self.QUESTION_NUMBER, str(lst)[1:-1].replace(' ',''), str(expected_output))
