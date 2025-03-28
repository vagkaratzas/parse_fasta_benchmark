# parse_fasta_benchmark
pyfastx vs biopython

## Comment
This script reads an input fasta file, iterates over all elements and changes their description, and finally writes out the updated sequences.
Three different modes are tested: pyfastx with index, pyfastx without index and biopython SeqIO.
In the current code, both pyfastx functions write out the sequence in one line, while SeqIO breaks it into lines of 60 amino acids.

### Verdict
If you are going to use the same `.fasta` file more than once, create the index (`.fxi` file) and copy it to your working directory, along with the `.fasta` file; if the properly named `.fxi` is already there, pyfastx won't rebuild it.
If you are just going to access random proteins by id, and not iterate though all proteins, again, use the index mode (not tested here).
If your fasta changes per execution, and you just want to iterate and parse all its elements, use pyfastx without building the index.

## Execution times
The input used for these benchmark was the UniProtKB Swiss-Prot dataset `uniprot_sprot.fasta`.
```
pyfastx version: 2.2.0
Biopython version: 1.84
Benchmark Results:
Pyfastx:          {'read': 0.6235275268554688   , 'modify': 1.7649967670440674, 'write': 0.3771960735321045 , 'total': 2.7657203674316406}
Pyfastx-prebuilt: {'read': 0.008824586868286133 , 'modify': 1.97509765625     , 'write': 0.25633978843688965, 'total': 2.240262031555176 }
Pyfastx-no Index: {'read': 0.0038051605224609375, 'modify': 0.8673803806304932, 'write': 0.3526613712310791 , 'total': 1.2238469123840332}
Biopython:        {'read': 3.1464295387268066   , 'modify': 2.2272427082061768, 'write': 1.4000837802886963 , 'total': 6.77375602722168  }
```
