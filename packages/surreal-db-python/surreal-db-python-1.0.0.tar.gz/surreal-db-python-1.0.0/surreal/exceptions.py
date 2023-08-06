class HTTPError(Exception):
    def __init__(self, status_code, message):
        """Raise HTTP Errors.

        Args:
            status_code (int): Status Code
            message (str): Message to show
        """
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
