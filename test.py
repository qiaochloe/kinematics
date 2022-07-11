import unittest
from kinematics import *


class IntegerArithmeticTestCase(unittest.TestCase):
    def testCaseOne(self):  # test method names begin with 'test'
        var_dict = {"deltax": "deltax", "v0": 0.0, "v": "v", "a": 3.2, "t": 32.8}
        equation_solver(var_dict)
        self.assertEqual(
            var_dict, {"deltax": 1721.344, "v0": 0.0, "v": 104.960, "a": 3.2, "t": 32.8}
        )

    def testCaseTwo(self):
        var_dict = {"deltax": 0, "v0": 1, "v": "v", "a": -2, "t": "t"}


if __name__ == "__main__":
    unittest.main()
