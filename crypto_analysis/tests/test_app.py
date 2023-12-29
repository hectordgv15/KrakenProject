import unittest

from crypto_analysis.app import CryptoAnalysisApp


class TestCryptoAnalysisApp(unittest.TestCase):
    def setUp(self):
        self.app = CryptoAnalysisApp()

    def test_init(self):
        self.assertTrue(self.app.model is not None)
        self.assertTrue(self.app.config is not None)
        self.assertTrue(isinstance(self.app.config, dict))

    def test_display_title(self):
        self.app.display_title()
        self.assertTrue(True)

    def test_display_sidebar(self):
        self.app.display_sidebar()
        self.assertTrue(self.app.filtered_data is not None)
        self.assertTrue(self.app.selected_asset is not None)

    def test_display_additional_info(self):
        self.app.display_sidebar()
        self.app.display_additional_info()
        self.assertTrue(True)

    def test_display_graph(self):
        self.app.display_sidebar()
        self.app.display_graph()
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
