class CryptoAnalysisException(Exception):
    """
    Exception class for crypto analysis errors.
    """

    def __init__(self, error_message, error_location):
        super().__init__(error_message)
        self.error_message = self.error_message_detail(error_message, error_location)

    def __str__(self):
        return self.error_message

    @staticmethod
    def error_message_detail(error, error_location):
        """
        Creates a detailed error message with the given error and error location.
        """
        error_message = f"Error ocurred [{error_location}] -> {str(error)}"
        return error_message
