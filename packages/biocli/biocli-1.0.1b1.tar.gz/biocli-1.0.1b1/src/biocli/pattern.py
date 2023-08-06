#!/usr/bin/env python3


"""
Pattern feature for finding given pattern in the given DNA or RNA sequence.
"""


from biocli._common._sequence import Sequence

__all__ = ["match"]


def match(pattern: str, text_file: str) -> list:
    """
    Checks for the presence of a pattern in the sequence.

    Args:
        pattern (str): The pattern to search for.
        text_file (str): The full file path to the sequence file.

    Return: Position indices of the pattern in the sequence.
    """

    seq = Sequence(text_file)

    positions = []

    for i in range(len(seq) - len(pattern) + 1):
        if seq[i : i + (len(pattern))] == pattern.upper():
            positions.append(i)

    print(positions)
    return positions
