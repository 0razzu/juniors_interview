import unittest

try:
    from task1.solution import strict
except ImportError as e:
    raise unittest.SkipTest("Task 1 is not completed yet")


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def contains_n_spaces(s: str, n: int, exactly: bool) -> bool:
    return (exactly and s.count(' ') == n) or (not exactly and s.count(' ') >= n)


class TestTask1(unittest.TestCase):
    def test_args_only_no_error(self):
        sum_two(1, 2)
        sum_two(-1, 0)
        contains_n_spaces('hello world', 1, True)
        contains_n_spaces('hello world', 2, False)

    def test_args_only_with_errors(self):
        with self.assertRaises(TypeError):
            sum_two(1, 2.4)
        with self.assertRaises(TypeError):
            sum_two(1)
        with self.assertRaises(TypeError):
            sum_two(1.1, 2)
        with self.assertRaises(TypeError):
            sum_two(1.1, 2.2)
        with self.assertRaises(TypeError):
            sum_two("1", 2)
        with self.assertRaises(TypeError):
            sum_two(7, True)
        with self.assertRaises(TypeError):
            contains_n_spaces(9, 1, True)
        with self.assertRaises(TypeError):
            contains_n_spaces('hello', 1.1, True)
        with self.assertRaises(TypeError):
            contains_n_spaces('hello', 1, 'w')

    def test_with_kwargs_no_error(self):
        sum_two(1, b=2)
        sum_two(a=-1, b=0)
        contains_n_spaces('hello world', 1, exactly=True)
        contains_n_spaces('hello world', n=1, exactly=True)
        contains_n_spaces(s='hello world', exactly=False, n=2)

    def test_with_kwargs_with_errors(self):
        with self.assertRaises(TypeError):
            sum_two(1, b=2.4)
        with self.assertRaises(TypeError):
            sum_two(1.1, b=2)
        with self.assertRaises(TypeError):
            sum_two(b="1", a=2)
        with self.assertRaises(TypeError):
            sum_two(a=7, b=True)
        with self.assertRaises(TypeError):
            contains_n_spaces(exactly=9, s=1, n=True)
        with self.assertRaises(TypeError):
            contains_n_spaces('hello', 1.1, exactly=True)
        with self.assertRaises(TypeError):
            contains_n_spaces('hello', n=1, exactly='w')
