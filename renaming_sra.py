#!/usr/bin/env python3

from Bio import SeqIO
import sys, os, re, gzip


def renaming_sra(files):

    for file in files:
        fastq = gzip.open(file, "rt")

        records = SeqIO.parse(fastq, "fastq")

        for record in records:
            name = str(record.name)
            description = str(record.description)
            break

        fastq.close()

        read_file = description.replace(name,"").split(":")[0]
        read_file = read_file.replace(" ","")

        print(read_file)

        # import pdb; pdb.set_trace()

        if read_file == "1":

            os.rename(file,(file.split("_")[0]).split(".")[0]+"_R1.fastq.gz")
            print("Read => " + read_file)
        elif read_file == "3":
            os.rename(file,(file.split("_")[0]).split(".")[0]+"_R2.fastq.gz")
            print("Read => " + read_file)
        else:
            os.rename(file,(file.split("_")[0]).split(".")[0]+"_I1.fastq.gz")
            print("Read => " + read_file)






if __name__ == '__main__':
    files = sys.argv[1:]
    print("Files read\n")
    for file in files:
        print(file)

    renaming_sra(files)
