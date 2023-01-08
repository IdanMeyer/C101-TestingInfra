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

    output_list = result.split('Mirror Linked list:')[1].strip().split()
    output_list = [int(x) for x in output_list]

    assert len(output_list) == len(expected_output_list)
    assert output_list == expected_output_list


def mirror(li_in):
    # Remove all negative numbers
    li_in = [x for x in li_in if x>=0]
    li_in = li_in[::-1]

    return li_in[::-1] + li_in

class TestQuestion1(object):
    def test_sanity(self):
        execute_ex5_test([1616, 25, 13, 12, -6], [1616, 25, 13,12,12,13,25,1616])
        execute_ex5_test([1,1,2,1,-1], [1,1,2,1,1,2,1,1])
        execute_ex5_test([1,-1], [1, 1])

    def test_pythonic(self):
        lst = [1616, 25, 13, 12]
        negative_number = random.randint(-1000, -1)
        lst.append(negative_number)

        execute_ex5_test(lst, mirror(lst))


    @pytest.mark.parametrize('number_of_items',range(1, 30))
    @pytest.mark.parametrize('iter_number',range(15))
    def test_automatic(self, iter_number, number_of_items):
        negative_number = random.randint(-1000, -1)

        lst = random.sample(range(0, 2**30), number_of_items)
        random.shuffle(lst)

        lst.append(negative_number)
        execute_ex5_test(lst, mirror(lst))
