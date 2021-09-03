'''
    This function is able to retrive info about the fastq file
'''
import sys, gzip
from Bio import SeqIO

def fastqinfo(file):
    with gzip.open(file, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            return(record)
            break
    
if __name__ == "__main__":
    file = sys.argv[1]

    record = fastqinfo(file)
    print(record)
