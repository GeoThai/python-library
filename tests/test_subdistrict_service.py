import unittest
from geothai import (
    get_all_subdistricts,
    get_subdistrict_by_id,
    get_subdistricts_by_criterion
)


class TestSubdistrictService(unittest.TestCase):
    def test_should_retrieve_all_subdistricts(self):
        subdistricts = get_all_subdistricts()
        self.assertIsInstance(subdistricts, list)
        self.assertGreater(len(subdistricts), 0)

    def test_should_retrieve_a_subdistrict_by_id(self):
        subdistrict_id = 100101
        subdistrict = get_subdistrict_by_id(subdistrict_id)
        self.assertIsNotNone(subdistrict)
        self.assertEqual(subdistrict['subdistrict_id'], subdistrict_id)

    def test_should_return_none_for_an_invalid_subdistrict_id(self):
        invalid_subdistrict_id = 99999
        subdistrict = get_subdistrict_by_id(invalid_subdistrict_id)
        self.assertIsNone(subdistrict)

    def test_should_retrieve_subdistricts_by_a_specific_criterion(self):
        criterion = {'subdistrict_name_en': 'Phra Borom Maha Ratchawang'}
        subdistricts = get_subdistricts_by_criterion(criterion)
        self.assertIsInstance(subdistricts, list)
        self.assertGreater(len(subdistricts), 0)
        self.assertEqual(
            subdistricts[0]['subdistrict_name_en'],
            'Phra Borom Maha Ratchawang'
        )

    def test_should_return_an_empty_list_for_a_non_matching_criterion(self):
        criterion = {'subdistrict_name_en': 'Non-Existent Subdistrict'}
        subdistricts = get_subdistricts_by_criterion(criterion)
        self.assertIsInstance(subdistricts, list)
        self.assertEqual(len(subdistricts), 0)


if __name__ == '__main__':
    unittest.main()
