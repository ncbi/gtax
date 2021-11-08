import unittest

from gtax.gtax_main import check_preexisting_data


class TestGtaxMethods(unittest.TestCase):

    def test_preexisting_data(self):
        self.assertRaises(Exception, check_preexisting_data)


if __name__ == '__main__':
    unittest.main()
