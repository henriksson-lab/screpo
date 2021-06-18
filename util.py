from typing import List, Optional, NamedTuple

import requests
import sys
import urllib
import subprocess
import pandas as pd
from pathlib import Path
from io import StringIO
from tqdm import tqdm
import shutil

import config


################################
# Merge multiple BAM/SAM/CRAM into one output file.
# outformat can be BAM SAM CRAM
def mergeBAM(infiles, outfile, outformat="BAM"):
    subprocess.call(["samtools", "merge", "-O", outformat, outfile, infiles], shell=True)


################################
# One bam split into two fastq.gz
def bamToFastq(bamfile, outfile_r1, outfile_r2):
    subprocess.call(
        ["samtools", "fastq", "-c", "6", "-1", outfile_r1, "-2", outfile_r2, "-0", "/dev/null", "-s", "/dev/null",
         "-n"])


################################   TODO!!!!!!!!!!!!!!!
# Merge and split
def mergeAndWriteSplitFastq(infiles: List[str], outfile_r1: Path, outfile_r2: Path):
    cmd = 'samtools cat ' + " ".join(infiles) + ' | samtools fastq -0 /dev/null -s /dev/null -n -c 1' \
        ' -1 ' + str(outfile_r1) + ' -2 ' + str(outfile_r2)
    print(cmd)
    subprocess.Popen(['sh', '-c',cmd], stdout=subprocess.PIPE).communicate()


################################
# Given column _filename and _10xsampleid, figure out which files should be merged and/or converted to 10x-suitable format.
# Perform the ops and put them in the right place
def smartmergeFilesFor10x(datasetdir, table):
    dir10x = datasetdir / "rawfq"
    listsamples = set(table["_10xsampleid"].tolist())
    for s in listsamples:
        print("Getting and processing files for sample " + s)
        listfiles = table[table["_10xsampleid"] == s]["_filename"].tolist()

        # What should the final files be called?
        # See here for reference: https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/fastq-input
        path_r1 = dir10x / s / (s + "_S1_L001_R1_001.fastq.gz")
        path_r2 = dir10x / s / (s + "_S1_L001_R2_001.fastq.gz")
        (dir10x / s).mkdir(parents=True, exist_ok=True)

        # Process files
        mergeAndWriteSplitFastq(listfiles, path_r1, path_r2)


################################
# Feedback class for providing a progress bar
class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


################################
# Download a file while showing a progress bar.
# output_path should be the name of the file, not the directory it goes into
def download_url(url: str, output_path: Path):
    if fake_download:
        if ".fq.gz" in url or ".fastq.gz" in url:
            thefile = "testdata/R1.fq.gz"
            if "R1" in url or "r1" in url:
                thefile = "testdata/R1.fq.gz"
            elif "R2" in url or "r2" in url:
                thefile = "testdata/R2.fq.gz"
            elif "I1" in url or "i1" in url:
                thefile = "testdata/I1.fq.gz"
            elif "_1" in url:
                thefile = "testdata/R1.fq.gz"
            elif "_2" in url:
                thefile = "testdata/R2.fq.gz"
            shutil.copyfile(thefile, output_path)
        elif ".bam" in url or ".cram" in url:
            thefile = "testdata/little.bam"
        else:
            # empty file as a backup
            open(output_path, 'a').close()
    else:
        print("Getting "+url)
        print()
        with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
            urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


# change to enable download testing
fake_download = False


################################
# Download an EGA dataset
# TODO test
def downloadEGA(id: str, outdir: Path):
    conf = config.getCellbusterConfig()
    egaconf = "~/.ega.json"
    if "pyega3config" in conf:
        egaconf = conf["pyega3config"]

    subprocess.call(["pyega3", "--saveto", outdir, "--delete-temp-files", "-cf", egaconf, "fetch", id], shell=True)
