#!/usr/bin/env python3

"""
Helper functions defined here.
"""
from datetime import datetime
from typing import Union


def _new_name(seq_type: str) -> Union[str, None]:

    """
    Creates a new file name based on the sequence type.
    """

    tstamp = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")

    if seq_type.lower() == "dna":
        return f"dna_sequence_{tstamp}.txt"
    if seq_type.lower() == "rna":
        return f"rna_sequence_{tstamp}.txt"
    print("Invalid sequence type. Choose RNA or DNA.")
    return "Failed!"


def save(seq_type: str, text: str) -> None:
    """
    Save the sequence to a file.
    """

    with open(str(_new_name(seq_type)), "w+", encoding="utf-8") as file:
        file.write(text)
    print("Saved successfully!")
