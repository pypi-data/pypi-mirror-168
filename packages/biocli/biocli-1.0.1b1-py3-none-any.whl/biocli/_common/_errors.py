#!/usr/bin/env python3


"""
Common errors defined here:
"""


class WrongFormatError(Exception):
    """Raised when the input file is not in the correct format"""

    def __init__(self, *args, **kwargs):
        default_message = (
            "The file you passed is not supported! Only .txt files are accepted."
        )

        # If any arguments are passed...
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else:
            # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)


class EmptyFileError(Exception):
    """Raised when the input file is empty"""

    def __init__(self, *args, **kwargs):
        default_message = "The file you passed is EMPTY!"

        # If any arguments are passed...
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else:
            # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)


class WrongNucleotideError(Exception):
    """Raised when the input file contains wrong nucleotides"""

    def __init__(self, *args, **kwargs):
        default_message = "The file you passed contains wrong set of nucleotides!"

        # If any arguments are passed...
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else:
            # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)
