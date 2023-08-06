"""
In this module will be defined all the ways to clean the input data.

The cleaning process is done by the Cleaner class.
"""

from pymink._exceptions import PyMinkException

from typing import Optional

class Cleaner:
    """
    This class is used to clean the input text.
    Diferent cleaning processes could be implemented.

    Cleaning process:

        Process 1:
            - Remove all non-alphanumeric characters
            - Remove all digits
            - Turn all characters to upper case

            Exceptions:
                - the '-' character will only be removed if it starts or ends a word
                - the ''' (apostrophe) character will only be removed if it stars or ends a word

            Examples:
                1- "gato," -> "GATO"
                2- "comprar-lhe" -> "COMPRAR-LHE"
                3- "togetheer" -> "TOGETHEER"
                4- "older'" -> "OLDER"
                4- "it?" -> "IT"
    """

    def __init__(self, process: str = "Process 1") -> None:
        self.process = process

    def clean(self, text: str, process: Optional[str] = None) -> str:
        """
        This method cleans the input text.
        """
        if not process:
            process = self.process

        if process == "Process 1":
            return ''.join([char for char in text if char.isalpha() or char == " "]).upper()
        else:
            raise PyMinkException(f"The process '{process}' is not implemented.")