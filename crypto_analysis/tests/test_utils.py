import unittest
import pandas as pd
from datetime import datetime, timedelta

from crypto_analysis.utils import select_box_date, process_response


class TestUtils(unittest.TestCase):
    def setUp(self):
        response_data = [
            [1641340800, "45", "47", "42", "43", "44", "40", 10],
            [1641427200, "43", "43", "42", "43", "43", "47", 20],
            [1641513600, "43", "43", "40", "41", "41", "57", 15],
        ]
        self.response = {"error": [], "result": {"BTCUSD": response_data, "last": 1641513600}}

        self.date_df = pd.DataFrame(
            [
                pd.to_datetime(1698364800, unit="s"),
                pd.to_datetime(1698451200, unit="s"),
                pd.to_datetime(1698537600, unit="s"),
                datetime.today() + timedelta(days=2),
            ],
            columns=["date"],
        )

    def test_process_response(self):
        output_data = [
            [pd.to_datetime(1641340800, unit="s"), 45, 47, 42, 43, 40],
            [pd.to_datetime(1641427200, unit="s"), 43, 43, 42, 43, 47],
            [pd.to_datetime(1641513600, unit="s"), 43, 43, 40, 41, 57],
        ]
        expected_output = pd.DataFrame(output_data, columns=["date", "open", "high", "low", "close", "volume"])
        output = process_response(self.response)
        self.assertTrue(all(output == expected_output))

    def test_select_box_date(self):
        expected_output = [pd.to_datetime(1698364800, unit="s"), datetime.today() + timedelta(days=2)]
        self.assertTrue(select_box_date(self.date_df), expected_output)


if __name__ == "__main__":
    unittest.main()
