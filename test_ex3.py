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

    # def test_only_negative_numbers(self):
    #     execute_ex3_test(self.QUESTION_NUMBER, "-1", "1")
    #     execute_ex3_test(self.QUESTION_NUMBER, "-1,-2,-3", "1")
    #     execute_ex3_test(self.QUESTION_NUMBER, "-30,-70,-85", "1")

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

    @pytest.mark.parametrize('iter_number',range(1, 99))
    @pytest.mark.parametrize('number_of_items',range(1, 7))
    def test_automated(self, iter_number, number_of_items):
        lst = [random.randint(-100, +100) for x in range(number_of_items-1)] + [random.randint(1, +100)]
        random.shuffle(lst)
        print(f"input number: {lst}")
        expected_output = self.get_max_sublist(lst)
        print(f"expected_output: {expected_output}")
        execute_ex3_test(self.QUESTION_NUMBER, str(lst)[1:-1].replace(' ',''), str(expected_output))


class TestQuestion2(object):
    QUESTION_NUMBER = 2

    def execute_ex3_q2_test(self, array, k, expected_output):
        if type(array) == list:
            array = str(array)[1:-1].replace(' ','')
        input_string = f"{array}{os.linesep}{k}{os.linesep}"
        execute_ex3_test(self.QUESTION_NUMBER, input_string, str(expected_output))

    def test_sanity(self):
        self.execute_ex3_q2_test("2,1,5,6,3", "3", 1)

    def test_examples(self):
        self.execute_ex3_q2_test("2,1,5,6,3", "3", 1)
        self.execute_ex3_q2_test("2,7,9,5,8,7,4", "5", 2)

    def test_all_numbers_already_match(self):
        self.execute_ex3_q2_test("1,2,3", "10", 0)
        self.execute_ex3_q2_test([1,2,3,4], 4, 0)
        self.execute_ex3_q2_test([1,1,1,1,1,1], 1, 0)
        self.execute_ex3_q2_test([1,20,20,20], 1, 0)
        self.execute_ex3_q2_test([1,1,20,20,20], 1, 0)

    def test_no_numbers_match_at_all(self):
        self.execute_ex3_q2_test([10,11,12,13], 1, 0)
        self.execute_ex3_q2_test([10,11,12,13], 5, 0)
        self.execute_ex3_q2_test([10,11,12,13], 9, 0)

    def min_swaps_from_internet(self, arr, n, k) :
        count = 0
        for i in range(0, n) :
            if (arr[i] <= k) :
                count = count + 1

        # Find unwanted elements
        # in current window of
        # size 'count'
        bad = 0
        for i in range(0, count) :
            if (arr[i] > k) :
                bad = bad + 1

        # Initialize answer with
        # 'bad' value of current
        # window
        ans = bad
        j = count
        for i in range(0, n) :

            if(j == n) :
                break

            # Decrement count of
            # previous window
            if (arr[i] > k) :
                bad = bad - 1

            # Increment count of
            # current window
            if (arr[j] > k) :
                bad = bad + 1

            # Update ans if count
            # of 'bad' is less in
            # current window
            ans = min(ans, bad)

            j = j + 1

        return ans

    @pytest.mark.parametrize('iter_number',range(1, 100))
    @pytest.mark.parametrize('number_of_items',range(1, 10))
    @pytest.mark.parametrize('k',range(1, 10))
    def test_automated(self, iter_number, number_of_items, k):
        lst = [random.randint(1, 20) for x in range(number_of_items)]
        print(f"input number: {lst}")
        print(f"k number: {k}")
        expected_output = self.min_swaps_from_internet(lst, len(lst), k)
        print(f"expected_output: {expected_output}")
        self.execute_ex3_q2_test(lst, k, expected_output)


class TestQuestion3(object):
    QUESTION_NUMBER = 3

    def test_sanity(self):
        execute_ex3_test(self.QUESTION_NUMBER, "2,3,1,2,3", "1")

    def test_examples(self):
        execute_ex3_test(self.QUESTION_NUMBER, "2,3,1,2,3", "1")
        execute_ex3_test(self.QUESTION_NUMBER, "0,3,1,2", "-1")

    @pytest.mark.parametrize('iter_number',range(1, 100))
    @pytest.mark.parametrize('number_of_items',range(1, 14))
    def test_no_duplicates(self, iter_number, number_of_items):
        lst = [x for x in range(number_of_items)]
        random.shuffle(lst)
        print(f"input list: {lst}")
        execute_ex3_test(self.QUESTION_NUMBER, str(lst)[1:-1].replace(' ',''), "-1")

    @pytest.mark.parametrize('iter_number',range(1, 20))
    @pytest.mark.parametrize('number_of_items',range(1, 10))
    def test_single_duplicate(self, iter_number, number_of_items):
        lst = [x for x in range(number_of_items)]
        # Adding a single duplicate item
        dup_item = random.choice(lst)
        lst.append(dup_item)

        random.shuffle(lst)
        print(f"input list: {lst}")
        execute_ex3_test(self.QUESTION_NUMBER, str(lst)[1:-1].replace(' ',''), "1")

    @pytest.mark.parametrize('iter_number',range(1, 20))
    @pytest.mark.parametrize('number_of_items',range(1, 10))
    @pytest.mark.parametrize('number_of_duplicates',range(1, 4))
    def test_multiple_duplicate(self, iter_number, number_of_items, number_of_duplicates):
        lst = [x for x in range(number_of_items)]
        # Adding a single random item
        for _ in range(number_of_duplicates):
            dup_item = random.choice(lst)
            lst.append(dup_item)

        random.shuffle(lst)
        print(f"input list: {lst}")
        execute_ex3_test(self.QUESTION_NUMBER, str(lst)[1:-1].replace(' ',''), "1")


class TestQuestion4(object):
    QUESTION_NUMBER = 4

    def test_sanity(self):
        execute_ex3_test(self.QUESTION_NUMBER, "4,0,0,2,0,5", "14")

    def test_examples(self):
        execute_ex3_test(self.QUESTION_NUMBER, "4,0,0,2,0,5", "14")
        execute_ex3_test(self.QUESTION_NUMBER, "4,0,0,4,0,5", "12")

    def test_examples_from_internet(self):
        execute_ex3_test(self.QUESTION_NUMBER, "3,0,2,0,4", "7")
        execute_ex3_test(self.QUESTION_NUMBER, "0,1,0,2,1,0,1,3,2,1,2,1", "6")

    def test_adding_zeros_at_edges(self):
        execute_ex3_test(self.QUESTION_NUMBER, "4,0,0,2,0,5", "14")
        execute_ex3_test(self.QUESTION_NUMBER, "0,4,0,0,2,0,5", "14")
        execute_ex3_test(self.QUESTION_NUMBER, "0,0,4,0,0,2,0,5", "14")
        execute_ex3_test(self.QUESTION_NUMBER, "0,0,4,0,0,2,0,5,0", "14")
        execute_ex3_test(self.QUESTION_NUMBER, "0,0,4,0,0,2,0,5,0,0", "14")
        execute_ex3_test(self.QUESTION_NUMBER, "4,0,0,2,0,5,0,0", "14")

    def test_asymetrical_walls(self):
        execute_ex3_test(self.QUESTION_NUMBER, "1,0,0,7", "2")
        execute_ex3_test(self.QUESTION_NUMBER, "7,0,0,1", "2")

        execute_ex3_test(self.QUESTION_NUMBER, "2,0,0,100", "4")
        execute_ex3_test(self.QUESTION_NUMBER, "100,0,0,2", "4")

    def max_water_from_internet(self, arr, n):
        # To store the maximum water
        # that can be stored
        res = 0

        # For every element of the array
        for i in range(1, n - 1):

            # Find the maximum element on its left
            left = arr[i]
            for j in range(i):
                left = max(left, arr[j])

            # Find the maximum element on its right
            right = arr[i]

            for j in range(i + 1, n):
                right = max(right, arr[j])

            # Update the maximum water
            res = res + (min(left, right) - arr[i])

        return res

    @pytest.mark.parametrize('iter_number',range(1, 50))
    @pytest.mark.parametrize('number_of_items',range(1, 10))
    @pytest.mark.parametrize('max_int', [20])
    def test_automated(self, max_int, iter_number, number_of_items):
        lst = [random.randint(0, max_int) for _ in range(number_of_items)]
        print(f"input list: {lst}")
        expected_output = self.max_water_from_internet(lst, len(lst))
        print(f"expected_output: {expected_output}")
        execute_ex3_test(self.QUESTION_NUMBER, str(lst)[1:-1].replace(' ',''), str(expected_output))

    @pytest.mark.parametrize('iter_number',range(1, 50))
    @pytest.mark.parametrize('number_of_items',range(1, 10))
    @pytest.mark.parametrize('max_int', [4])
    def test_automated_small_numbers(self, max_int, iter_number, number_of_items):
        lst = [random.randint(0, max_int) for _ in range(number_of_items)]
        print(f"input list: {lst}")
        expected_output = self.max_water_from_internet(lst, len(lst))
        print(f"expected_output: {expected_output}")
        execute_ex3_test(self.QUESTION_NUMBER, str(lst)[1:-1].replace(' ',''), str(expected_output))
