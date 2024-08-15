import unittest
from geothai import (
    get_all_provinces,
    get_province_by_id,
    get_provinces_by_criterion
)


class TestProvinceService(unittest.TestCase):
    def test_should_retrieve_all_provinces(self):
        provinces = get_all_provinces()
        self.assertIsInstance(provinces, list)
        self.assertGreater(len(provinces), 0)

    def test_should_retrieve_a_province_by_id(self):
        province_id = 10
        province = get_province_by_id(province_id)
        self.assertIsNotNone(province)
        self.assertEqual(province['province_id'], province_id)

    def test_should_return_none_for_an_invalid_province_id(self):
        invalid_province_id = 99999
        province = get_province_by_id(invalid_province_id)
        self.assertIsNone(province)

    def test_should_retrieve_provinces_by_a_specific_criterion(self):
        criterion = {'province_name_en': 'Bangkok'}
        provinces = get_provinces_by_criterion(criterion)
        self.assertIsInstance(provinces, list)
        self.assertGreater(len(provinces), 0)
        self.assertEqual(provinces[0]['province_name_en'], 'Bangkok')

    def test_should_return_an_empty_list_for_a_non_matching_criterion(self):
        criterion = {'province_name_en': 'Non-Existent Province'}
        provinces = get_provinces_by_criterion(criterion)
        self.assertIsInstance(provinces, list)
        self.assertEqual(len(provinces), 0)


if __name__ == '__main__':
    unittest.main()
