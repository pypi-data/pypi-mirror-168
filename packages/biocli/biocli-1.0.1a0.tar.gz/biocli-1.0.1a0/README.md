
# CLI tool for Computational Biology

	Please read before use!

    Works with python version >= 3.9
    For Linux users only
    Works with `.txt` files only.
    Install requirements via pip3.
    Make the "compute" file executable using linux terminal typing `chmod +x compute` command

## How to use

Examples:
```console
$ ./compute biocli -h
usage: compute biocli [-h] {count,pattern,translate}
    
positional arguments:
  {count,pattern,translate}
    count                    Count feature to count the nucleotides and patterns in the 
                             given DNA or RNA sequence.
    pattern                  Pattern feature for finding given pattern in the given DNA 
                             or RNA sequence.
    translate                Translate feature to translate the given DNA sequence to 
                             RNA and vice versa.

optional arguments:
    -h, --help                 show this help message and exit
```
```console
$ ./compute biocli translate dna-to-rna "sample.txt" to_file=False
UGCUCCGCCGAACCAUUCAUGCGGGAUACGACUUGGAUGACAUAGGAAAUUCAUAAUUAUCGUGUCUAAGUAAUUGCAUGCAGGCUGCAA
UAACGUUGUUGGCCGAGCGUAAUACAAGAUUAGCCGCUGUUGAUGCUCAUUAGACGCGUUGGUAAAUUUGACGUUCUUAUGACCCCUACG
UAUAACAGAAUAGCCUCUGGUGACUUUUCUGAGCACCGAUCUCGCAAUAUAUUAGCCACUAUAUUAUCUAAGCCGAGCCAAUCAUUGAUA
CACAUAGUAAUGUCAGGACGUCGAACCUAGAUUGUAUGACUCCGCUAAGGUAUUCCGAGAGACACUAGGAUACUAGAUAUAUUCCCAAAG
UAAGGCGACGCCUAGUCUUUAGAGAGCGAGUAUGCCUUUGCCAAGUGUUGGAUGAGCCCGCCCCUUAAUAGGUGCUACGCUAGAGGCAAA
GCAUGUGGGCGGUGGCCACACUUCAAUCAGGUGGCGAGUAGACGCUUCAGCCCGUUCGAUCUUAAGUAUCAGUAUAGGGACUCGAGUACA
GUGUCCAAAUUACUGCGCUCGGUCCUAUGCUGACAAGGCGAACUCUGCAGAGAAUGGUCCGAAUUCACAUUCGGACAAUACGAUGUAGGA
CCGAACAAGCACAGUUUGAUUCGCCUCGGAAGACGGUGCAACUGAAACAGUAGAUCUCCUUAUCAAUGUAGGGCGAAGUACUGCCCGCGU
GAGGGCACCAGCAUCCAGUCUCGUUGCUGUUCGUAUGGGGAUCAACGGCGGGUUGUUCUUAAGAACAUCAGGAUGAGUUAAUCGAGAGUA
CUGAACCGCUAUUCGACACCGCAGGUUGCGACACCAAAUUGCCUAAACAUCAACAGCCUCAAUUACCUGCUGUCCACUCGAGCUUGGGGU
ACAGUGUUAUCCUUCACUUGAACGACAAGAUAAUGAACAUUGUGGACUUGCGUAUA
```


## Project layout
```console
├── biocli
   ├── biocli
   │   ├── count.py
   │   ├── pattern.py 
   │   ├── translate.py 
   │   ├── _errors.py
   │   ├── _helper.py
   │   ├── _sequence.py
   │   ├── __init__.py
   ├── compute 

```

### Contains:

	DNA to RNA sequence translator
	RNA to DNA sequence translator
	Pattern matcher
	Pattern counter
	Nucleotide counter
	Frequency counter

	Sample files added.

Built on top of DynaCLI by BST Labs. [Check it out!](https://github.com/BstLabs/py-dynacli)

