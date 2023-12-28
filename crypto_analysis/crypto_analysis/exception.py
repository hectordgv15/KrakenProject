def error_message_detail(error, error_location):
    error_message = f"Error ocurred in: [{str(error)}]"

    return error_message


class DashboardException(Exception):
    def __init__(self, error_message, error_location):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_location)

    def __str__(self):
        return self.error_message
