import os
import sys
import pytest
import math
from math import sqrt
import random
import re
import itertools

import Infra
import tempfile, shutil, os


def create_temporary_copy(path, p,q,r,exact=False):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'temp_file.c')
    # shutil.copy2(path, temp_path)

    fin = open(path)
    fout = open(temp_path, "wt")
    for line in fin:
        if exact:
            line = line.replace("Point p = { .x = 10, .y = 20 };", "Point p = { .x = %s, .y = %s };"%(p[0], p[1]))
            line = line.replace("Point q = { .x = 40, .y = -20 };", "Point q = { .x = %s, .y = %s };"%(q[0], q[1]))
            line = line.replace("Point r = { .x = 5, .y = 5 };", "Point r = { .x = %s, .y = %s };"%(r[0], r[1]))
        else:
            line = line.replace("Point p = { .x = 10, .y = 20 };", "Point p = { .x = %g, .y = %g };"%(p[0], p[1]))
            line = line.replace("Point q = { .x = 40, .y = -20 };", "Point q = { .x = %g, .y = %g };"%(q[0], q[1]))
            line = line.replace("Point r = { .x = 5, .y = 5 };", "Point r = { .x = %g, .y = %g };"%(r[0], r[1]))
        fout.write(line)
    fin.close()
    fout.close()

    return temp_path

compiled_path = None
# @pytest.fixture(scope='session', autouse=True)
def compile(c_file_path):
    compiled_path = Infra.compile_if_needed(c_file_path, force=True)
    return compiled_path


def execute_ex4_test(c_path, p,q,r,exact=False):

    # Modify file
    tmp_copy = create_temporary_copy(c_path, p,q,r, exact=exact)

    compiled_path = compile(tmp_copy)

    a = math.sqrt( ((p[0]-q[0])**2)+((p[1]-q[1])**2) ) # p,q
    b = math.sqrt( ((p[0]-r[0])**2)+((p[1]-r[1])**2) ) # p,r
    c = math.sqrt( ((q[0]-r[0])**2)+((q[1]-r[1])**2) ) # q,r
    perimeter = a+b+c
    s = (a+b+c)/2
    area = (s*(s-a)*(s-b)*(s-c)) ** 0.5

    is_right_angle = sqrt(a**2)==sqrt(b**2+c**2) or sqrt(b**2)==sqrt(a**2+c**2) or sqrt(c**2)==sqrt(a**2+b**2)


    if is_right_angle:
        is_right_angle_str = "a right angle triangle"
    else:
        is_right_angle_str = "not a right angle triangle"

    expected_output = "The perimeter of a triangle with corners (%g, %g), (%g, %g) and (%g, %g) is %g%s"%(p[0], p[1], q[0],q[1],r[0],r[1], perimeter, os.linesep)
    expected_output += "The area of a triangle with corners (%g, %g), (%g, %g) and (%g, %g) is %g%s"%(p[0], p[1], q[0],q[1],r[0],r[1], area, os.linesep)
    expected_output += "The triangle with corners (%g, %g), (%g, %g) and (%g, %g) is %s%s"%(p[0], p[1], q[0],q[1],r[0],r[1], is_right_angle_str, os.linesep)


    input_string = f""
    result = Infra.execute_c_bin(compiled_path, input_string).decode()
    print(result)
    print(expected_output)
    assert result == expected_output


def check_all_permutations(path, p,q,r):
    prems = list(itertools.permutations([p,q,r]))
    for p,q,r in prems:
        execute_ex4_test(path, p,q,r)


class TestQuestion1(object):
    def test_sanity(self, request):
        execute_ex4_test(request.config.option.path, (10,20),(-20,40),(5,5))
        execute_ex4_test(request.config.option.path, (0,0),(0,13),(13,0))

    def test_right_angles(self, request):
        execute_ex4_test(request.config.option.path, (3,0),(4,-1),(1,-2))
        execute_ex4_test(request.config.option.path, (3,0),(6,4),(-1,3))
        execute_ex4_test(request.config.option.path, (0,0),(4,0),(2,2))
        execute_ex4_test(request.config.option.path, (2,5),(-2,-3),(10,1))
        execute_ex4_test(request.config.option.path, (1,3),(-1,1),(3,1))
        execute_ex4_test(request.config.option.path, (3,1),(4,4),(6,0))
        execute_ex4_test(request.config.option.path, (0,0),(0,4),(3,0))
        execute_ex4_test(request.config.option.path, (0,0),(0,2),(3,0))
        execute_ex4_test(request.config.option.path, (5,7),(2,1),(4,0))
        execute_ex4_test(request.config.option.path, (-60,1),(-60,2),(-80,2))
        execute_ex4_test(request.config.option.path, (0,0),(5,1),(4,6))
        execute_ex4_test(request.config.option.path, (-4,1),(-4,-1),(10,1))
        execute_ex4_test(request.config.option.path, (-4,11),(-4,9),(10,11))
        execute_ex4_test(request.config.option.path, (1.5, 11),(1.5, 9),(15.5,11))
        execute_ex4_test(request.config.option.path, (1.5, 9),(3.5, 9),(3.5,-5))

    def test_non_right_angles(self, request):
        execute_ex4_test(request.config.option.path, (2,2),(3,9),(7,5))
        execute_ex4_test(request.config.option.path, (1,3),(4,2),(-2,1))
        execute_ex4_test(request.config.option.path, (0,0),(4,0),(3,2))
        execute_ex4_test(request.config.option.path, (0,0),(0,5),(-19, 5.9))
        execute_ex4_test(request.config.option.path, (0,0),(0,5),(-19, 5.999))
        execute_ex4_test(request.config.option.path, (0,0),(0.001,5),(-19, 5))

    def test_different_order_points(self, request):
        execute_ex4_test(request.config.option.path, (-2, 1),(2, -2),(5,2))
        execute_ex4_test(request.config.option.path, (2, -2),(-2, 1),(5,2))
        execute_ex4_test(request.config.option.path, (5,2),(2, -2),(-2, 1))
        execute_ex4_test(request.config.option.path, (5,2),(-2, 1),(2, -2))
        execute_ex4_test(request.config.option.path, (2, -2),(5,2),(-2, 1))
        execute_ex4_test(request.config.option.path, (-2, 1),(5,2),(2, -2))

    def test_more_examples(self, request):
        execute_ex4_test(request.config.option.path, (0,0),(1,0),(0.5,0.5))
        execute_ex4_test(request.config.option.path, (0,0),(1,0),(0.5,-0.5))
        execute_ex4_test(request.config.option.path, (0,0),(0,-1),(0.5,-0.5))
        execute_ex4_test(request.config.option.path, (0,0),(0,-2),(1,-1))

    def test_non_rational_number(self, request):
        execute_ex4_test(request.config.option.path, (0,0),(0,-2*sqrt(2)),(sqrt(2), -sqrt(2)), exact=True)
        execute_ex4_test(request.config.option.path, (0,0),(-sqrt(2),-2*sqrt(2)),(0, -sqrt(2)), exact=True)
        execute_ex4_test(request.config.option.path, (0,0),(-sqrt(2)+1,-sqrt(2)),(0, -2*sqrt(2)), exact=True)


    def test_different_permutations(self, request):
        p = (10,1)
        q = (-4,1)
        r = (10,-1)
        check_all_permutations(request.config.option.path, p, q, r)

    @pytest.mark.parametrize('iter_number',range(10))
    def test_random_points(self, request, iter_number):
        low_end = -10000
        high_end = 10000
        p = ( random.uniform(low_end, high_end),  random.uniform(low_end, high_end))
        q = ( random.uniform(low_end, high_end),  random.uniform(low_end, high_end))
        r = ( random.uniform(low_end, high_end),  random.uniform(low_end, high_end))
        execute_ex4_test(request.config.option.path, p,q,r, exact=True)

    @pytest.mark.parametrize('iter_number',range(10))
    def test_random_sqrt_points(self, request, iter_number):
        low_end = 0
        high_end = 1000
        p = ( sqrt(random.uniform(low_end, high_end)),  sqrt(random.uniform(low_end, high_end)))
        q = ( sqrt(random.uniform(low_end, high_end)),  sqrt(random.uniform(low_end, high_end)))
        r = ( sqrt(random.uniform(low_end, high_end)),  sqrt(random.uniform(low_end, high_end)))
        execute_ex4_test(request.config.option.path, p,q,r, exact=True)

    # @pytest.mark.parametrize('iter_number',range(300))
    # def test_random_points_stress(self, request, iter_number):
    #     low_end = -10000
    #     high_end = 10000
    #     p = ( random.uniform(low_end, high_end),  random.uniform(low_end, high_end))
    #     q = ( random.uniform(low_end, high_end),  random.uniform(low_end, high_end))
    #     r = ( random.uniform(low_end, high_end),  random.uniform(low_end, high_end))
    #     execute_ex4_test(request.config.option.path, p,q,r, exact=True)

