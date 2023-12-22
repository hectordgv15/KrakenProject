import unittest

# from dashboard import # TODO
from utils import select_box_date
from analysis_class import Analysis


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.input_1 = []
        self.input_2 = []

    def test_select_box_date(self):
        expected_output = []
        self.assertEqual(select_box_date(self.input_1), expected_output)


class TestAnalysisClass(unittest.TestCase):
    def setUp(self):
        self.analysis = Analysis()
        self.input_1 = []
        self.input_2 = []

    def test_get_data(self):
        expected_output = []

        self.assertEqual(self.analysis.get_data(self.input_1), expected_output)
        self.assertEqual(self.analysis.get_data(self.input_2), expected_output)

    def test_compute_indicators(self):
        expected_output = []

        self.assertEqual(self.analysis.compute_indicators(self.input_1), expected_output)
        self.assertEqual(self.analysis.compute_indicators(self.input_2), expected_output)


if __name__ == "__main__":
    unittest.main()
