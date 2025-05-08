import unittest
from geothai import (
    get_all_districts,
    get_district_by_code,
    get_districts_by_criterion,
    District
)


class TestDistrictService(unittest.TestCase):
    def test_should_retrieve_all_districts(self):
        districts = get_all_districts()
        self.assertIsInstance(districts, list)
        self.assertGreater(len(districts), 0)

    def test_should_retrieve_a_district_by_code(self):
        district_code = '1001'
        district = get_district_by_code(district_code)
        self.assertIsNotNone(district)
        self.assertEqual(district['code'], int(district_code))

    def test_should_return_none_for_an_invalid_district_code(self):
        invalid_district_code = '99999'
        district = get_district_by_code(invalid_district_code)
        self.assertIsNone(district)

    def test_should_retrieve_districts_by_a_specific_criterion(self):
        criterion: District = {'name_en': 'Phra Nakhon'}
        districts = get_districts_by_criterion(criterion)
        self.assertIsInstance(districts, list)
        self.assertGreater(len(districts), 0)
        self.assertEqual(districts[0]['name_en'], 'Phra Nakhon')

    def test_should_return_an_empty_list_for_a_non_matching_criterion(self):
        criterion: District = {'name_en': 'Non-Existent District'}
        districts = get_districts_by_criterion(criterion)
        self.assertIsInstance(districts, list)
        self.assertEqual(len(districts), 0)


if __name__ == '__main__':
    unittest.main()
