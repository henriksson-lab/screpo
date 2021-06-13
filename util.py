import requests
import sys
import urllib
import subprocess
import pandas as pd
from pathlib import Path
from io import StringIO
from tqdm import tqdm

import config

################################
# Merge multiple BAM/SAM/CRAM into one output file.
# outformat can be BAM SAM CRAM
def mergeBAM(infiles, outfile, outformat="BAM"):
    subprocess.call(["samtools", "merge", "-O", outformat, outfile, infiles],shell=True)


################################
# One bam split into two fastq.gz
def bamToFastq(bamfile, outfile_r1, outfile_r2):
    subprocess.call(["samtools","fastq","-c","6","-1",outfile_r1,"-2",outfile_r2,"-0","/dev/null","-s","/dev/null","-n"])

################################   TODO!!!!!!!!!!!!!!!
# Merge and split
def mergeAndWriteSplitFastq(infiles, outfile_r1, outfile_r2):
    open(outfile_r1, 'a').close() #create empty file for now
    open(outfile_r2, 'a').close() #create empty file for now

#how to do this in python? does it work?
#samtools cat *.bam | samtools fastq -c 6 -1 foo_r1.fastq.gz foo_r2.fastq.gz


################################
# Download an EGA dataset
# TODO test
def downloadEGA(id):
    conf = config.getCellbusterConfig()
    if "pyega3config" in conf:
        egaconf = conf["pyega3config"]
        subprocess.call(["pyega3", "-cf", egaconf, "fetch", id],shell=True)
    else:
        subprocess.call(["pyega3", "fetch", id],shell=True)

################################
# Given column _filename and _10xsampleid, figure out which files should be merged and/or converted to 10x-suitable format.
# Perform the ops and put them in the right place
def smartmergeFilesFor10x(datasetdir, table):
    dir10x = datasetdir / "rawfq"
    listsamples = set(table["_10xsampleid"].tolist())
    for s in listsamples:
        print("Getting and processing files for sample "+s)
        listfiles = table[table["_10xsampleid"]==s]["_filename"].tolist()

        #What should the final files be called?
        #See here for reference: https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/fastq-input
        path_r1 = dir10x / s / (s+"_S1_L001_R1_001.fastq.gz")
        path_r2 = dir10x / s / (s+"_S1_L001_R2_001.fastq.gz")
        (dir10x / s).mkdir(parents=True,exist_ok=True)

        #Process files
        mergeAndWriteSplitFastq(listfiles, path_r1, path_r2)





################################
# Feedback class for providing a progress bar
class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

################################
# Download a file while showing a progress bar
def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

