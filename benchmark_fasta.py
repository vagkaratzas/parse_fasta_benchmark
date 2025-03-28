#!/usr/bin/env python3

import time
import pyfastx
import Bio
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys

def benchmark_pyfastx(fasta_file, output_file):
    times = {}
    
    # Measure reading time
    start = time.time()
    fasta = pyfastx.Fasta(fasta_file)
    times['read'] = time.time() - start
    
    # Measure modifying descriptions time
    start = time.time()
    modified_records = [(seq.name, seq.seq, f"Modified_{' '.join(seq.description.split()[1:])}") for seq in fasta]
    times['modify'] = time.time() - start
    
    # Measure writing time
    start = time.time()
    with open(output_file, 'w') as f:
        for name, seq, desc in modified_records:
            f.write(f">{name} {desc}\n{seq}\n")
    times['write'] = time.time() - start
    
    times['total'] = sum(times.values())
    return times

def benchmark_pyfastx_no_index(fasta_file, output_file):
    times = {}
    
    # Measure reading time
    start = time.time()
    fasta = pyfastx.Fasta(fasta_file, build_index=False, full_name=True)
    times['read'] = time.time() - start
    
    # Measure modifying descriptions time
    start = time.time()
    modified_records = [(name.split()[0], seq, f"Modified_{' '.join(name.split()[1:])}") for name, seq in fasta]
    times['modify'] = time.time() - start
    
    # Measure writing time
    start = time.time()
    with open(output_file, 'w') as f:
        for name, seq, desc in modified_records:
            f.write(f">{name} {desc}\n{seq}\n")
    times['write'] = time.time() - start
    
    times['total'] = sum(times.values())
    return times

def benchmark_biopython(fasta_file, output_file):
    times = {}
    
    # Measure reading time
    start = time.time()
    records = list(SeqIO.parse(fasta_file, "fasta"))
    times['read'] = time.time() - start
    
    # Measure modifying descriptions time
    start = time.time()
    modified_records = [SeqRecord(rec.seq, id=rec.id, description=f"Modified_{' '.join(rec.description.split()[1:])}") for rec in records]
    times['modify'] = time.time() - start
    
    # Measure writing time
    start = time.time()
    with open(output_file, 'w') as f:
        SeqIO.write(modified_records, f, "fasta")
    times['write'] = time.time() - start
    
    times['total'] = sum(times.values())
    return times

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python benchmark_fasta.py <fasta_file>")
        sys.exit(1)
    
    fasta_file = sys.argv[1]
    
    print("pyfastx version:", pyfastx.__version__)
    print("Biopython version:", Bio.__version__)

    pyfastx_times = benchmark_pyfastx(fasta_file, "output_pyfastx.fasta")
    pyfastx_times_prebuilt = benchmark_pyfastx(fasta_file, "output_pyfastx_prebuilt.fasta") # doesn't re-create index, if .fxi file already there
    pyfastx_times_no_index = benchmark_pyfastx_no_index(fasta_file, "output_pyfastx_no_index.fasta")
    biopython_times = benchmark_biopython(fasta_file, "output_biopython.fasta")
    
    print("Benchmark Results:")
    print("Pyfastx:", pyfastx_times)
    print("Pyfastx-prebuilt:", pyfastx_times_prebuilt)
    print("Pyfastx-no Index:", pyfastx_times_no_index)
    print("Biopython:", biopython_times)
