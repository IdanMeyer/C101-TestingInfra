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


def execute_ex4_test(a,b,c, expected_output):
    input_string = f"{a}{os.linesep}{b}{os.linesep}{c}{os.linesep}{os.linesep}"
    result = Infra.execute_c_bin(compiled_path, input_string).decode()
    assert result == expected_output


# def convert_equation_to_numbers(quadratic_equation):
#     quadratic_equation_matcher = re.compile(r'(-?\d+)x\^2([+-]\d+)x([+-]\d+)')
#     matches = quadratic_equation_matcher.match(quadratic_equation)
#     if None != matches:
#         a = int(matches.group(1))
#         b = int(matches.group(2))
#         c = int(matches.group(3))
#     else:
#         linear_equation_matcher = re.compile(r'([+-]\d+)x([+-]\d+)')
#         matches = linear_equation_matcher.match(quadratic_equation)
#         if None != matches:
#             a = 0
#             b = int(matches.group(1))
#             c = int(matches.group(2))

#     return a,b,c

def solve_quadratic_equation(a,b,c):
    if a==0 and b ==0 and c ==0:
        return "has infinite real roots"
    if a==0:
        return "has one real root: %g"  %(-c/b+0)
    d = b**2 - 4*a*c
    x1 = (-b + d**0.5)/(2*a)
    x2 = (-b - d**0.5)/(2*a)

    x1 += 0
    x2 += 0


    if type(x1) == complex and type(x2) == complex:
        return "has no real roots"
    elif x1 == x2:
        return "has one real root: %g"  %(x1)
    else:
        return "has two real roots: %g and %g"  %(x1, x2)

def execute_semi_automated_test(a,b,c,quadratic_equation):
    sol = solve_quadratic_equation(a,b,c)
    expected_output = f"Please enter three numbers:\n{quadratic_equation} = 0 {sol}\n"
    execute_ex4_test(a,b,c, expected_output)


class TestQuestion1(object):

    def test_sanity(self):
        execute_ex4_test(1,2,3, "Please enter three numbers:\nx^2+2x+3 = 0 has no real roots\n")

    def test_examples(self):
        execute_ex4_test(1,2,1, "Please enter three numbers:\nx^2+2x+1 = 0 has one real root: -1\n")
        execute_ex4_test(1,5,6, "Please enter three numbers:\nx^2+5x+6 = 0 has two real roots: -2 and -3\n")
        execute_ex4_test(0,0,0, "Please enter three numbers:\n0 = 0 has infinite real roots\n")
        execute_ex4_test(2,0,2, "Please enter three numbers:\n2x^2+2 = 0 has no real roots\n")
        execute_ex4_test(1,-1,2, "Please enter three numbers:\nx^2-x+2 = 0 has no real roots\n")
        execute_ex4_test(0,1,2, "Please enter three numbers:\nx+2 = 0 has one real root: -2\n")

    def test_more_examples(self):
        execute_semi_automated_test(1,0,1, "x^2+1")
        execute_semi_automated_test(1,0,-1, "x^2-1")
        execute_semi_automated_test(1,0,-2, "x^2-2")
        execute_semi_automated_test(-1,0,-2, "-x^2-2")
        execute_semi_automated_test(-1,0,-1, "-x^2-1")
        execute_semi_automated_test(-7,2,-1, "-7x^2+2x-1")
        execute_semi_automated_test(-7,2,1, "-7x^2+2x+1")
        execute_semi_automated_test(-1,0,1, "-x^2+1")
        execute_semi_automated_test(-7,2,0, "-7x^2+2x")
        execute_semi_automated_test(-7,2,0, "-7x^2+2x")
        execute_semi_automated_test(1,2,0, "x^2+2x")
        execute_semi_automated_test(1,0,0, "x^2")
        execute_semi_automated_test(2,0,0, "2x^2")
        execute_semi_automated_test(0,0,0, "0")
        execute_semi_automated_test(-1,1,0, "-x^2+x")
        execute_semi_automated_test(-1,1,-1, "-x^2+x-1")
        execute_semi_automated_test(-1,1,1, "-x^2+x+1")
        execute_semi_automated_test(-2,1,1, "-2x^2+x+1")
        execute_semi_automated_test(-2,2,1, "-2x^2+2x+1")
        execute_semi_automated_test(2,3,1, "2x^2+3x+1")
        execute_semi_automated_test(2,1,1, "2x^2+x+1")
        execute_semi_automated_test(2,1,-1, "2x^2+x-1")
        execute_semi_automated_test(0,1,2, "x+2")
        execute_semi_automated_test(0,1,0, "x")
        execute_semi_automated_test(0,2,0, "2x")
        execute_semi_automated_test(0,-2,0, "-2x")
        execute_semi_automated_test(0,-1,0, "-x")

    @pytest.mark.parametrize('b',range(-10, 10))
    @pytest.mark.parametrize('c',range(-10, 10))
    def test_linear(self, b, c):
        if b == 0 and c != 0:
            return
        if b==0 and c ==0:
            execute_semi_automated_test(0,b,c, f"0")
        elif b==1 and c>0:
            execute_semi_automated_test(0,b,c, f"x+{c}")
        elif b==1 and c<0:
            execute_semi_automated_test(0,b,c, f"x{c}")
        elif b==1 and c==0:
            execute_semi_automated_test(0,b,c, f"x")
        elif b==-1 and c>0:
            execute_semi_automated_test(0,b,c, f"-x+{c}")
        elif b==-1 and c<0:
            execute_semi_automated_test(0,b,c, f"-x{c}")
        elif b==-1 and c==0:
            execute_semi_automated_test(0,b,c, f"-x")
        elif c<0:
            execute_semi_automated_test(0,b,c, f"{b}x{c}")
        elif c==0:
            execute_semi_automated_test(0,b,c, f"{b}x")
        else:
            execute_semi_automated_test(0,b,c, f"{b}x+{c}")

    # @pytest.mark.parametrize('a',range(-10, 10))
    # @pytest.mark.parametrize('b',range(-10, 10))
    # @pytest.mark.parametrize('c',range(-10, 10))
    # def test_quad(self, a, b, c):
    #     if a==0:
    #         return
    #     if a==0 and b==0 and c ==0:
    #         execute_semi_automated_test(0,0,0, f"0")
    #     elif a == 1 and b>1 and c>=0:
    #         execute_semi_automated_test(a,b,c, f"x^2+{b}x+{c}")
    #     elif a == -1 and b>1 and c>=0:
    #         execute_semi_automated_test(a,b,c, f"-x^2+{b}x+{c}")
    #     elif a == 1 and b==1 and c>=0:
    #         execute_semi_automated_test(a,b,c, f"x^2+x+{c}")
    #     elif a == -1 and b==1 and c>=0:
    #         execute_semi_automated_test(a,b,c, f"-x^2+x+{c}")
    #     elif a > 1 and b==1 and c>=0:
    #         execute_semi_automated_test(a,b,c, f"{a}x^2+x+{c}")
    #     elif a < -1 and b==1 and c>=0:
    #         execute_semi_automated_test(a,b,c, f"{a}-x^2+x+{c}")

    #     elif a == 1 and b>1 and c<0:
    #         execute_semi_automated_test(a,b,c, f"x^2+{b}x{c}")
    #     elif a == -1 and b>1 and c<0:
    #         execute_semi_automated_test(a,b,c, f"-x^2+{b}x{c}")
    #     elif a == 1 and b==1 and c<0:
    #         execute_semi_automated_test(a,b,c, f"x^2+x{c}")
    #     elif a == -1 and b==1 and c<0:
    #         execute_semi_automated_test(a,b,c, f"-x^2+x{c}")
    #     elif a > 1 and b==1 and c<0:
    #         execute_semi_automated_test(a,b,c, f"{a}x^2+x{c}")
    #     elif a < -1 and b==1 and c<0:
    #         execute_semi_automated_test(a,b,c, f"{a}-x^2+x{c}")
    #     elif a > 1 and b>1 and c<0:
    #         execute_semi_automated_test(a,b,c, f"{a}x^2+{b}x{c}")
    #     elif a < -1 and b<1 and c<0:
    #         execute_semi_automated_test(a,b,c, f"{a}x^2{b}{c}")

    #     else:
    #         execute_semi_automated_test(a,b,c, f"{a}x^2+{b}x+{c}")


