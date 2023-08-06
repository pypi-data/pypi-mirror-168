#!/usr/bin/env python3


"""
Translate feature to translate the given DNA sequence to RNA and vice versa.
"""


from biocli._common._errors import WrongNucleotideError
from biocli._common._helper import save
from biocli._common._sequence import Sequence

__all__ = ["dna_to_rna", "rna_to_dna"]


def dna_to_rna(text_file: str, to_file: bool = False) -> str:
    """
    Translates the DNA sequence to RNA.

    Args:
        text_file (str): The full file path to the sequence file.
        to_file (bool): Save to file option. Default is False.

    Return: RNA sequence
    """

    seq = Sequence(text_file)

    # check if the sequence is DNA
    if seq.is_rna():
        raise WrongNucleotideError

    rna_text = "".join(["U" if x == "T" else x for x in seq])

    if to_file:
        save("RNA", rna_text)
    else:
        print(rna_text)

    return rna_text


def rna_to_dna(text_file: str, to_file: bool = False) -> str:
    """
    Translates the DNA sequence to RNA.

    Args:
        text_file (str): The full file path to the sequence file.
        to_file (bool): Save to file option. Default is False.

    Return: DNA sequence
    """

    seq = Sequence(text_file)

    # check if the sequence is RNA
    if seq.is_dna():
        raise WrongNucleotideError

    dna_text = "".join(["T" if x == "U" else x for x in seq])

    if to_file:
        save("DNA", dna_text)
    else:
        print(dna_text)

    return dna_text
