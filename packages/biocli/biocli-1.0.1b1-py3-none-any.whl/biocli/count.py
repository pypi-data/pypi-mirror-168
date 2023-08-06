#!/usr/bin/env python3


"""
Count feature to count the nucleotides and patterns in the given DNA or RNA sequence.
"""


from collections import Counter
from typing import Dict

from biocli._common._sequence import Sequence

__all__ = ["nucleotide", "pattern", "frequency"]


def nucleotide(text_file: str) -> Counter:
    """
    Counts all the nucleotides in the sequence separately.

    Args:
        text_file (str): The full file path to the sequence file.

    Return:  Nucleotides and their counts.
    """

    seq = Sequence(text_file)

    counts = Counter([seq])

    for symbol, count in sorted(counts.items()):
        print(f"{symbol} -- {count}")

    return counts


def pattern(pattern_: str, text_file: str) -> str:
    """
    Counts the number of occurance of the pattern in given text file.

    Args:
        pattern (str): The pattern to search for.
        text_file (str): The full file path to the sequence file.

    Return: Count of pattern.
    """

    seq = Sequence(text_file)

    return f"{str(seq).count(pattern_)} patterns found."


def frequency(window_len: int, text_file: str) -> Dict:
    """

    Counts all the possible nucleotide combinations of given length in the sequence.

    Args:
        text_file (str): The full file path to the sequence file
        window_len (int): The length of the nucleotide combination.

    Return: Nucleotide combinations and their counts.
    """

    seq = Sequence(text_file)

    frequency_ = {}

    for i in range(len(seq) - window_len + 1):
        pattern_ = seq[i : i + window_len]
        frequency_[pattern_] = 0

        for j in range(len(seq) - window_len + 1):
            if seq[j : (j + window_len)] == pattern_:
                frequency_[pattern_] += 1

    for freq, value in frequency_.items():
        print(f"{freq} -- {value}")

    return frequency_
