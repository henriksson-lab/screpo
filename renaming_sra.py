#!/usr/bin/env python3

from Bio import SeqIO
import sys, os, re, gzip


def renaming_sra(file1,file2):
    fastq1 = gzip.open(file1, "rt")
    fastq2 = gzip.open(file2, "rt")

    records1 = SeqIO.parse(fastq1, "fastq")
    records2 = SeqIO.parse(fastq2, "fastq")

    for record in records1:
        name1 = str(record.name)
        description1 = str(record.description)
        break

    for record in records2:
        name2 = str(record.name)
        description2 = str(record.description)
        break


    read_file1 = description1.replace(name1,"").split(":")[0]
    read_file2 = description2.replace(name2,"").split(":")[0]

    print("read_file1")
    print(read_file1)
    print("read_file2")
    print(read_file2)
    # import pdb; pdb.set_trace()






if __name__ == '__main__':
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    renaming_sra(file1,file2)
