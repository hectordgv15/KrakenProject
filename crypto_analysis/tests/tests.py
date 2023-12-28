import unittest
import pandas as pd

# from dashboard import # TODO
from crypto_analysis.utils import select_box_date, process_response
from crypto_analysis.model import CryptoAnalysisModel
from crypto_analysis.app import CryptoAnalysisApp


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
        self.analysis = CryptoAnalysisModel()
        self.input_data = {"pair": "BTCUSD", "interval": 1440, "since": 1696118400, "until": 1696377600}

        data = {
            "date": [
                pd.to_datetime(1698364800, unit="s"),
                pd.to_datetime(1698451200, unit="s"),
            ],
            "open": [34155.2, 33915.1],
            "high": [34239.7, 34463.7],
            "low": [33318.6, 33852.8],
            "close": [33915.1, 34092.1],
            "volume": [2681.16178873, 1222.22173256],
            "MA": [29102.17692307692, 29355.684615384613],
            "period_high": [35225.0, 35225.0],
            "period_low": [26820.0, 26820.1],
            "pctK": [84.41522903033906, 86.52095801258788],
            "pctD": [87.80646459962247, 86.14130211372418],
            "Buy_Signal": [0, 0],
            "Sell_Signal": [0, 0],
            "Overbought_Signal": [0, 0],
            "Oversold_Signal": [0, 0],
        }

        # Crear DataFrame
        self.expected_output = pd.DataFrame(data, columns=data.keys())

    def test_get_conection(self):
        self.analysis.get_conection()
        self.assertTrue(self.analysis.connection is not None)

    def test_load_config(self):
        self.analysis.load_config()
        self.assertTrue(self.analysis.config is not None)
        self.assertTrue(isinstance(self.analysis.config, dict))

    def test_get_data(self):
        output_data = self.analysis.get_data(**self.input_data)

        expected_output_0 = [pd.to_datetime(1696204800, unit="s"), 27981.1, 28572.5, 27298.0, 27500.9, 5477.09708743]
        expected_output_1 = [pd.to_datetime(1696291200, unit="s"), 27500.9, 27658.2, 27189.0, 27428.2, 2269.82042802]

        self.assertTrue(len(output_data) > 0)
        self.assertTrue(all(output_data.columns == ["date", "open", "high", "low", "close", "volume"]))
        self.assertTrue(all(output_data.loc[0] == expected_output_0))
        self.assertTrue(all(output_data.loc[1] == expected_output_1))

        self.assertTrue(len(self.analysis.data_cache) > 0)
        self.assertTrue("raw" in self.analysis.data_cache[self.input_data["pair"]])

    def test_get_crypto_pairs(self):
        default_pairs = ["ETHUSD", "BTCUSD", "USDTUSD", "XRPUSD", "USDCUSD", "SOLUSD", "ADAUSD", "DOGEUSD", "TRXUSD"]
        pairs = self.analysis.get_crypto_pairs()
        self.assertTrue(set(default_pairs) <= set(pairs))

    def test_compute_indicators(self):
        _ = self.analysis.get_data(**self.input_data)
        output_data = self.analysis.compute_indicators(**self.input_data)

        self.assertTrue(len(output_data) > 0)
        self.assertTrue(all(output_data.columns == self.expected_output.columns))

        self.assertTrue(all(output_data.loc[0] == self.expected_output.loc[0]))
        self.assertTrue(all(output_data.loc[1] == self.expected_output.loc[1]))

        self.assertTrue(all(output_data["pctK"] >= 0) and all(output_data["pctK"] <= 100))
        self.assertTrue(all(output_data["pctD"] >= 0) and all(output_data["pctD"] <= 100))

        self.assertTrue(set(output_data["Buy_Signal"].unique()) <= {0, 1})
        self.assertTrue(set(output_data["Sell_Signal"].unique()) <= {0, 1})

        self.assertTrue(set(output_data["Overbought_Signal"].unique()) <= {0, 1})
        self.assertTrue(set(output_data["Oversold_Signal"].unique()) <= {0, 1})

        self.assertTrue(len(self.analysis.data_cache) > 0)
        self.assertTrue("data" in self.analysis.data_cache[self.input_data["pair"]])

    def test_graph_pair(self):
        fig = self.analysis.graph_pair(self.expected_output, "BTCUSD")
        self.assertTrue(fig is not None)


if __name__ == "__main__":
    unittest.main()
