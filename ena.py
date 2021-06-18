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

import enaBrowserTools.enaDataGet

#######################################################
#######################################################
#all metadata
#curl -v "https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=SRP312953"
#including column "Run" looking like SRR14121712
#######################################################
#######################################################


def getRunInfo(id):
    r = requests.get('https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term='+id).content.decode('utf-8')
    return pd.read_csv(StringIO(r), sep=",")

print(getRunInfo("SRP312953"))

##################################################

#curl -v "https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=SRR000001"

### from ena, assume we want get ERR3510662

## conda install enaBrowserTools

#https://www.ebi.ac.uk/ena/browser/api/xml/<accession>


#enaBrowserTools.enaDataGet.enaget_main(["-f","fastq","SRR14121712"])
#enaBrowserTools.enaDataGet.enaget_main(["ena SRR14121712 -f fastq"])



#enaDataGet -f fastq -d <destination/directory> ERR164409


#wget "https://www.ebi.ac.uk/ena/browser/api/xml/ERR3510662"
#wget "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=ERR3510662&result=read_run&fields=run_accession,submitted_ftp,submitted_md5,submitted_bytes,submitted_format"
#wget "ftp.sra.ebi.ac.uk/vol1/run/ERR351/ERR3510662/SM1_S1_L004.bam"


########################################################
# assume we have the id "ERS2852885" --- now what?


