import unittest
import pandas as pd

# from dashboard import # TODO
from utils import select_box_date, process_response
from analysis_class import Analysis


class TestUtils(unittest.TestCase):
    def setUp(self):
        response_data = [
            [1641340800, "45", "47", "42", "43", "44", "40", 10],
            [1641427200, "43", "43", "42", "43", "43", "47", 20],
            [1641513600, "43", "43", "40", "41", "41", "57", 15],
        ]
        self.response = {"error": [], "result": {"BTCUSD": response_data, "last": 1641513600}}

        self.input_2 = []

    def test_process_response(self):
        output_data = [
            [pd.to_datetime(1641340800, unit="s"), 45, 47, 42, 43, 40],
            [pd.to_datetime(1641427200, unit="s"), 43, 43, 42, 43, 47],
            [pd.to_datetime(1641513600, unit="s"), 43, 43, 40, 41, 57],
        ]
        expected_output = pd.DataFrame(output_data, columns=["date", "open", "high", "low", "close", "volume"])
        output = process_response(self.response)
        # TODO: mirar si hay una mejor forma para comparar pandas DF
        self.assertTrue(all(output == expected_output))

    # TODO: TBD elegimos fechas o no?
    # def test_select_box_date(self):
    #     expected_output = []
    #     self.assertEqual(select_box_date(self.input_1), expected_output)


class TestAnalysisClass(unittest.TestCase):
    def setUp(self):
        self.analysis = Analysis()
        self.input_data = {"pair": "BTCUSD", "interval": 1440, "since": 1696118400, "until": 1696377600}

    def test_get_data(self):
        output_data = self.analysis.get_data(**self.input_data)

        expected_output_0 = [pd.to_datetime(1696204800, unit="s"), 27981.1, 28572.5, 27298.0, 27500.9, 5477.09708743]
        expected_output_1 = [pd.to_datetime(1696291200, unit="s"), 27500.9, 27658.2, 27189.0, 27428.2, 2269.82042802]

        self.assertTrue(len(output_data) > 0)
        self.assertTrue(all(output_data.columns == ["date", "open", "high", "low", "close", "volume"]))
        self.assertTrue(all(output_data.loc[0] == expected_output_0))
        self.assertTrue(all(output_data.loc[1] == expected_output_1))

    # def test_compute_indicators(self):
    #     expected_output = []

    #     self.assertEqual(self.analysis.compute_indicators(self.input_1), expected_output)
    #     self.assertEqual(self.analysis.compute_indicators(self.input_2), expected_output)


if __name__ == "__main__":
    unittest.main()
