'''
    This function is able to retrive info about the fastq file
'''
import sys, re, gzip
from Bio import SeqIO

def fastqinfo(file):
    if re.search(".gz",file):
        container = gzip.open(file, "rt")
    else:
        container = open(file,"rt")

    with container as handle:
        for record in SeqIO.parse(handle, "fastq"):
            return(record)
            break
    
if __name__ == "__main__":
    file = sys.argv[1]

    record = fastqinfo(file)
    print(record)
