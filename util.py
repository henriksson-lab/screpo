from typing import List, Optional, NamedTuple

import json
import urllib
import subprocess
from pathlib import Path
from tqdm import tqdm
import shutil
from tempfile import gettempdir
import os

import config


################################
# Check if a variable is NaN (works on any type)
def isNaN(num):
    return num != num


################################
# Merge multiple BAM/SAM/CRAM into one output file.
# outformat can be BAM SAM CRAM
def mergeBAM(infiles, outfile, outformat="BAM"):
    subprocess.call(["samtools", "merge", "-O", outformat, outfile, infiles], shell=True)


################################
# One bam split into two fastq.gz
def bamToFastq(bamfile, outfile_r1, outfile_r2):
    subprocess.call(
        ["samtools", "fastq", "-c", "6", "-1", outfile_r1, "-2", outfile_r2, "-0", "/dev/null", "-s", "/dev/null", "-n"])


################################
# Merge and split
def mergeAndWriteSplitFastq(infiles: List[str], outfile_r1: Path, outfile_r2: Path):
    infiles = [str(x) for x in infiles]
    cmd = 'samtools cat ' + " ".join(infiles) + ' | samtools fastq - -0 /dev/null -s /dev/null -n -c 1' \
        ' -1 ' + str(outfile_r1) + ' -2 ' + str(outfile_r2)
    print(cmd)
    subprocess.Popen(['sh', '-c',cmd], stdout=subprocess.PIPE).communicate()


################################
# Given column _filename and _10xsampleid, figure out which files should be merged and/or converted to 10x-suitable format.
# Perform the ops and put them in the right place
def smartmergeFilesFor10x(datasetdir: Path, table):
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

        # TODO are the files BAM or CRAM? if fastq, need other tools for merging

        # Process files
        mergeAndWriteSplitFastq(listfiles, path_r1, path_r2)


################################
# Move a FASTQ-file to where it should be within a 10x directory structure
def moveFASTQto10x(datasetdir: Path, fname: Path, samplename: str):
    #"ftp.sra.ebi.ac.uk/vol1/fastq/SRR110/075/SRR11008275/SRR11008275_1.fastq.gz"

    if any([x in str(fname) for x in ["_1.fastq.gz","_R1.fastq.gz","_1.fq.gz","_R1.fq.gz"]]):
        new_fname = dir10x / samplename / (samplename + "_S1_L001_R1_001.fastq.gz")
    elif any([x in str(fname) for x in ["_2.fastq.gz", "_R2.fastq.gz", "_2.fq.gz", "_R2.fq.gz"]]):
        new_fname = dir10x / samplename / (samplename + "_S1_L001_R2_001.fastq.gz")
    elif any([x in str(fname) for x in ["_I1.fastq.gz", "_I1.fq.gz"]]):
        new_fname = dir10x / samplename / (samplename + "_S1_L001_I1_001.fastq.gz")
    else:
        raise Exception("Do not now how to rename "+str(fname))

    dir10x = datasetdir / "rawfq"
    (dir10x / s).mkdir(parents=True, exist_ok=True)
    fname.rename(new_fname)



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



################################
# Create a new temporary directory. Should only be used for small files.
# Delete after use
def createSystemTempDir() -> Path:
    tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
    os.makedirs(tmp)
    return Path(tmp)



################################
# Nicely print JSON on screen
def prettyPrintJSON(dat):
    print(json.dumps(dat, indent=4, sort_keys=True))


################################
# Turn [[...]] into [...]
def flatten(t):
    return [item for sublist in t for item in sublist]


def anyin(liststring: List[str], target: str):
    return any([s in target for s in liststring])

