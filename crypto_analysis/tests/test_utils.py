import unittest
import pandas as pd

from crypto_analysis.utils import select_box_date, process_response


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


if __name__ == "__main__":
    unittest.main()
