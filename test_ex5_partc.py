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
    input_string = f""
    for i in original_list:
        input_string += f"{i}{os.linesep}"
    result = Infra.execute_c_bin(compiled_path, input_string).decode()

    output_list = result.split('Linked list after duplicate removal:')[1].strip().split()
    output_list = [int(x) for x in output_list]

    assert len(output_list) == len(expected_output_list)
    assert output_list == expected_output_list


def remove_duplicates(li_in):
    # Remove all negative numbers
    li_in = [x for x in li_in if x>=0]
    li_in = li_in[::-1]

    return sorted([x for x in set(li_in)])[::-1]

class TestQuestion1(object):
    def test_sanity(self):
        execute_ex5_test([11, 11, 11, 13, 13, 20, -1], [20, 13, 11])
        execute_ex5_test([11, 11, 11, -1], [11])

    def test_pythonic(self):
        lst = [11, 11, 11, 13, 13, 20, -1]
        negative_number = -1
        lst.append(negative_number)

        execute_ex5_test(lst, remove_duplicates(lst))



    @pytest.mark.parametrize('number_of_items',range(1, 20))
    @pytest.mark.parametrize('iter_number',range(5))
    @pytest.mark.parametrize('min_number',[0, 6])
    @pytest.mark.parametrize('max_number',[8, 2**30])
    def test_automatic(self, iter_number, min_number, max_number, number_of_items):
        negative_number = random.randint(-1000, -1)
        lst = [random.randint(min_number,max_number) for x in range(number_of_items)]
        lst.sort()

        lst.append(negative_number)

        execute_ex5_test(lst, remove_duplicates(lst))
