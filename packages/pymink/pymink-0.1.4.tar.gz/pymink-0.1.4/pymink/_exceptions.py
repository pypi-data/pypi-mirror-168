"""This module wraps The Exception class to provide a more user-friendly interface."""

class PyMinkException(Exception):
    """This class wraps the Exception class to provide a more user-friendly interface."""

    def __init__(self, message: str) -> None:
        """This method initializes the PyMinkException class."""
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """This method returns the message of the exception."""
        return self.message

if __name__ == "__main__":
    raise PyMinkException("This is a test exception.")