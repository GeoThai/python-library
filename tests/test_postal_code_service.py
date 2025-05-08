import unittest
from geothai import (
    get_all_postal_codes,
    get_postal_codes_by_code
)


class TestPostalCodeService(unittest.TestCase):
    def test_should_retrieve_all_postal_codes(self):
        postal_codes = get_all_postal_codes()
        self.assertIsInstance(postal_codes, list)
        self.assertGreater(len(postal_codes), 0)

    def test_should_retrieve_a_postal_code_by_code(self):
        postal_code_code = '10200'
        postal_code = get_postal_codes_by_code(postal_code_code)
        self.assertIsNotNone(postal_code)
        self.assertEqual(postal_code['code'], int(postal_code_code))

    def test_should_return_none_for_an_invalid_postal_code_code(self):
        invalid_postal_code_code = '99999'
        postal_code = get_postal_codes_by_code(invalid_postal_code_code)
        self.assertIsNone(postal_code)


if __name__ == '__main__':
    unittest.main()
