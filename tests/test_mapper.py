import unittest
from mapper import build_query

class BuildQueryTests(unittest.TestCase):
    def test_build_query_with_strings(self):
        query = build_query(0, 0, 1, ["cafe", "restaurant"])
        self.assertIn('"amenity"="cafe"', query)
        self.assertIn('"amenity"="restaurant"', query)

    def test_build_query_with_dicts(self):
        tags = [{"key": "waterway", "value": "river"}]
        query = build_query(0, 0, 1, tags)
        self.assertIn('"waterway"="river"', query)

    def test_build_query_with_parking(self):
        tags = [{"key": "amenity", "value": "parking"}]
        query = build_query(0, 0, 1, tags)
        self.assertIn('"amenity"="parking"', query)

if __name__ == "__main__":
    unittest.main()
