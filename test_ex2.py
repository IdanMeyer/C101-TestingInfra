import os
import sys
import pytest
import math

import Infra

C_EXEC_PATH = "/tmp/exec"
sys.setrecursionlimit(1500)


def execute_ex2_test(question_number, question_input, expected_output):
    input_string = f"{question_number}{os.linesep}{question_input}{os.linesep}"
    result = Infra.execute_c_bin_and_parse_result(C_EXEC_PATH, input_string)
    assert result == expected_output


class TestQuestion1(object):
    QUESTION_NUMBER = 1

    def test_sanity(self):
        execute_ex2_test(self.QUESTION_NUMBER, 10, "1010")

    def test_examples(self):
        execute_ex2_test(self.QUESTION_NUMBER, 10, "1010")
        execute_ex2_test(self.QUESTION_NUMBER, 158, "10011110")
        execute_ex2_test(self.QUESTION_NUMBER, 1000, "1111101000")

    @pytest.mark.parametrize('num',range(0, 1024))
    def test_automated(self, num):
        print(f"input number: {num}")
        expected_output = bin(num)[2:]
        print(f"expected_output: {expected_output}")
        execute_ex2_test(self.QUESTION_NUMBER, num, expected_output)




class TestQuestion2(object):
    QUESTION_NUMBER = 2

    def question_2_alg(self, n):
        if n <=0:
            return 0
        if n == 1:
            return 1
        return math.sqrt(n + self.question_2_alg(n-1))


    def test_sanity(self):
        execute_ex2_test(self.QUESTION_NUMBER, 10, "3.675980")

    def test_examples(self):
        execute_ex2_test(self.QUESTION_NUMBER, 10, "3.675980")
        execute_ex2_test(self.QUESTION_NUMBER, 100, "10.509991")
        execute_ex2_test(self.QUESTION_NUMBER, 1000, "32.126479")

    @pytest.mark.parametrize('num',range(0, 1000))
    def test_automated(self, num):
        print(f"input number: {num}")
        # expected_output = str(round(self.question_2_alg(num), 6))
        expected_output = '{:.6f}'.format(self.question_2_alg(num))

        print(f"expected_output: {expected_output}")
        execute_ex2_test(self.QUESTION_NUMBER, num, expected_output)
