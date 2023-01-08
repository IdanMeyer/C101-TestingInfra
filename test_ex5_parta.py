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

    output_list = result.split('Modified Linked list:')[1].strip().split()
    output_list = [int(x) for x in output_list]

    assert len(output_list) == len(expected_output_list)
    assert output_list == expected_output_list


def odd_then_even(li_in):
    # Remove all negative numbers
    li_in = [x for x in li_in if x>=0]
    li_in = li_in[::-1]

    ev_li = [ele for ele in li_in if ele%2 ==0]
    od_li = [ele for ele in li_in if ele%2 !=0]
    return ev_li + od_li

class TestQuestion1(object):
    def test_sanity(self):
        execute_ex5_test([0, 1, 8, 667, 56, 250, 16, -1], [16, 250, 56, 8,0, 667, 1])
        execute_ex5_test([1000, 1, 8,667,56,250,13,-5], [250, 56, 8,1000, 13, 667, 1])


    @pytest.mark.parametrize('number_of_items',range(1, 30))
    @pytest.mark.parametrize('iter_number',range(10))
    def test_automatic(self, iter_number, number_of_items):
        negative_number = random.randint(-1000, -1)

        lst = [random.randint(0, 2**30) for x in range(number_of_items)]
        random.shuffle(lst)

        lst.append(negative_number)
        execute_ex5_test(lst, odd_then_even(lst))

    @pytest.mark.parametrize('number_of_items',range(1, 30))
    def test_odd_only(self, number_of_items):
        negative_number = random.randint(-1000, -1)

        lst = [random.randrange(1,2**30,2) for p in range(0,number_of_items)]
        random.shuffle(lst)

        lst.append(negative_number)
        execute_ex5_test(lst, odd_then_even(lst))

    @pytest.mark.parametrize('number_of_items',range(1, 30))
    def test_even_only(self, number_of_items):
        negative_number = random.randint(-1000, -1)

        lst = [random.randrange(0,9,2) for p in range(0,number_of_items)]
        random.shuffle(lst)

        lst.append(negative_number)
        execute_ex5_test(lst, odd_then_even(lst))
