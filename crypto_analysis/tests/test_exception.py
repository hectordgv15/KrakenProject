import unittest

from crypto_analysis.exception import CryptoAnalysisException


class TestCryptoAnalysisException(unittest.TestCase):
    def setUp(self):
        self.error_message = "This is an error message"
        self.error_location = "APP BUILD"

    def test_init(self):
        # Set exception
        exception = CryptoAnalysisException(self.error_message, self.error_location)

        # Check exception class
        self.assertTrue(exception.args[0] == self.error_message)
        self.assertTrue(str(exception) == f"Error ocurred [{self.error_location}] -> {self.error_message}")

    def test_str(self):
        # Set exception
        exception = CryptoAnalysisException(self.error_message, self.error_location)

        # Check __str__ method
        self.assertTrue(str(exception) == f"Error ocurred [{self.error_location}] -> {self.error_message}")

    def test_error_message_detail(self):
        # Set exception
        error = ValueError("Invalid input")
        exception = CryptoAnalysisException(error, self.error_location)

        # Get error message detailed
        exception.error_message_detail(error, self.error_location)

        # Check message detail
        self.assertTrue(exception.error_message == f"Error ocurred [{self.error_location}] -> {str(error)}")


if __name__ == "__main__":
    unittest.main()
