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



ENTERING_QUESTION = "Please choose a question by entering 1-5 (enter 0 to exit):"
def execute_ex6_1_test(question_number, question_input, expected_decimal):
    input_string = f"{question_number}{os.linesep}{question_input}{os.linesep}"
    result = Infra.execute_c_bin(compiled_path, input_string)
    decimal_number = result.decode().split(":")[-2].split(os.linesep)[0].strip()
    hex_number = result.decode().split(":")[-1].split(os.linesep)[0].strip()
    assert expected_decimal == int(decimal_number)
    assert expected_decimal == int(hex_number, 16)

def execute_ex6_2_test(question_number, num1, num2):
    input_string = f"{question_number}{os.linesep}{num1}{os.linesep}{num2}{os.linesep}"
    result = Infra.execute_c_bin(compiled_path, input_string)
    output_num1 = result.decode().split("num1=")[-1].split()[0].strip(',')
    output_num2 = result.decode().split("num2=")[-1].strip()
    assert num1 == int(output_num2)
    assert num2 == int(output_num1)

def execute_ex6_3_test(question_number, num1, expected_output):
    input_string = f"{question_number}{os.linesep}{num1}{os.linesep}"
    result = Infra.execute_c_bin(compiled_path, input_string)
    output = result.decode().split("Output: ")[-1].strip()
    assert expected_output == int(output)

def execute_ex6_4_test(question_number, num1):
    input_string = f"{question_number}{os.linesep}{num1}{os.linesep}"
    result = Infra.execute_c_bin(compiled_path, input_string)
    return "is a palindrome" in result.decode()


class TestQuestion1(object):
    QUESTION_NUMBER = 1

    def test_sanity(self):
        execute_ex6_1_test(self.QUESTION_NUMBER, "110011", 51)

    @pytest.mark.parametrize('number',range(1, 100))
    def test_automated(self, number):
        execute_ex6_1_test(self.QUESTION_NUMBER, bin(number)[2:], number)

    @pytest.mark.parametrize('number',range(1, 100))
    def test_random(self, number):
        number = random.randint(0, 2**31-1)
        execute_ex6_1_test(self.QUESTION_NUMBER, bin(number)[2:], number)

class TestQuestion2(object):
    QUESTION_NUMBER = 2

    def test_sanity(self):
        execute_ex6_2_test(self.QUESTION_NUMBER, 15, 10)

    @pytest.mark.parametrize('number1',range(1, 20))
    @pytest.mark.parametrize('number2',range(1, 20))
    def test_automated(self, number1, number2):
        execute_ex6_2_test(self.QUESTION_NUMBER, number1, number2)

    @pytest.mark.parametrize('number',range(1, 100))
    def test_random(self, number):
        number1 = random.randint(0, 2**31-1)
        number2 = random.randint(0, 2**31-1)
        execute_ex6_2_test(self.QUESTION_NUMBER, number1, number2)


class TestQuestion3(object):
    QUESTION_NUMBER = 3

    def nextPowerOf2(self, n):
        p = 1
        if (n and not(n & (n - 1))):
            return n
        while (p < n) :
            p <<= 1
        return p;

    def test_sanity(self):
        execute_ex6_3_test(self.QUESTION_NUMBER, 9, 16)
        execute_ex6_3_test(self.QUESTION_NUMBER, 8, 8)
        execute_ex6_3_test(self.QUESTION_NUMBER, 3, 4)

    @pytest.mark.parametrize('number',range(1, 100))
    def test_automated(self, number):
        execute_ex6_3_test(self.QUESTION_NUMBER, number, self.nextPowerOf2(number))

    @pytest.mark.parametrize('number',range(1, 100))
    def test_random(self, number):
        number = random.randint(0, 2**15)
        execute_ex6_3_test(self.QUESTION_NUMBER, number, self.nextPowerOf2(number))

class TestQuestion4(object):
    QUESTION_NUMBER = 4

    def test_sanity(self):
        assert True==execute_ex6_4_test(self.QUESTION_NUMBER, 9)
        assert False==execute_ex6_4_test(self.QUESTION_NUMBER, 10)

    @pytest.mark.parametrize('number',range(1, 100))
    def test_automated(self, number):
        bin_str = bin(number)[2:]
        is_palindrom = (bin_str ==bin_str[::-1])
        assert is_palindrom == execute_ex6_4_test(self.QUESTION_NUMBER, number)

    @pytest.mark.parametrize('number',range(1, 100))
    def test_random(self, number):
        number = random.randint(0, 2**15)
        bin_str = bin(number)[2:]
        is_palindrom = (bin_str ==bin_str[::-1])
        assert is_palindrom == execute_ex6_4_test(self.QUESTION_NUMBER, number)
