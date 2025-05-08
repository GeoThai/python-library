import json
import unittest
from geothai import metadata, Metadata

with open('geothai/data/metadata.json', "r", encoding="utf-8") as f:
    _expected_metadata: Metadata = json.load(f)


class TestDistrictService(unittest.TestCase):
    def test_should_match_the_expected_metadata(self):
        self.assertEqual(metadata, _expected_metadata)


if __name__ == '__main__':
    unittest.main()
