C_FILE_PATH = "<Path to your C file>"

import os
import sys
import pytest
import math

import Infra

# Setting a large recursion limit because it is needed at q2 and q3 algorithms
sys.setrecursionlimit(2000)



compiled_path = None
@pytest.fixture(scope='session', autouse=True)
def compile():
    global compiled_path
    compiled_path = Infra.compile_if_needed(C_FILE_PATH)


def execute_ex2_test(question_number, question_input, expected_output):
    input_string = f"{question_number}{os.linesep}{question_input}{os.linesep}"
    result = Infra.execute_c_bin_and_parse_result(compiled_path, input_string)
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

    @pytest.mark.parametrize('num',range(0, 1500))
    def test_automated(self, num):
        print(f"input number: {num}")
        expected_output = '{:.6f}'.format(self.question_2_alg(num))

        print(f"expected_output: {expected_output}")
        execute_ex2_test(self.QUESTION_NUMBER, num, expected_output)


class TestQuestion3(object):
    QUESTION_NUMBER = 3

    def question_3_alg(self, n, i=1):
        if n <=0:
            return 0
        if (i == n):
            return math.sqrt(i)
        return math.sqrt(i + self.question_3_alg(n, i+1))


    def test_sanity(self):
        execute_ex2_test(self.QUESTION_NUMBER, 3, "1.712265")

    def test_examples(self):
        execute_ex2_test(self.QUESTION_NUMBER, 10, "1.757933")
        execute_ex2_test(self.QUESTION_NUMBER, 100, "1.757933")
        execute_ex2_test(self.QUESTION_NUMBER, 1000, "1.757933")

    @pytest.mark.parametrize('num',range(0, 1500))
    def test_automated(self, num):
        print(f"input number: {num}")
        expected_output = '{:.6f}'.format(self.question_3_alg(num))

        print(f"expected_output: {expected_output}")
        execute_ex2_test(self.QUESTION_NUMBER, num, expected_output)
