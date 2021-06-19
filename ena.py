import requests
import pandas as pd
from io import StringIO
from pathlib import Path

import util

################################
# Download ERR to a file; return path to the file
def downloadEnaERR(id_err: str, tempdir: Path) -> Path:
    # Read metadata
    r = requests.get(
        "https://www.ebi.ac.uk/ena/portal/api/filereport?accession="+id_err+"&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,tax_id,scientific_name,fastq_ftp,submitted_ftp,sra_ftp&format=tsv&download=true"
    ).content.decode('utf-8')
    df = pd.read_csv(StringIO(r), sep="\t")

    # The different possible links
    url_submitted = df["submitted_ftp"].iloc[0]
    url_fastq = df["fastq_ftp"].iloc[0]
    url_sra = df["sra_ftp"].iloc[0]

    # Of the different links, which one to use?
    if not util.isNaN(url_submitted):
        urls = url_submitted
    elif not util.isNaN(url_fastq):
        urls = url_fastq
    elif not util.isNaN(url_sra):
        raise Exception("The data is only available at SRA; "+url_sra)
    else:
        raise Exception("No data for "+id_err)

    #This is a list of ;-separated files
    list_files=[]
    for url in urls.split(";"):

        # What should the downloaded filename be?
        fname = url.split("/")[-1]

        # Assume http if nothing else stated
        if not "://" in url:
            url = "http://"+url

        # Get the file
        downloaded_file = tempdir / fname
        util.download_url(url, downloaded_file)
        list_files.append(downloaded_file)

    return list_files






################################
# For testing
def main():
    util.fake_download = True
    tempdir = util.getTempDir()
    fnames = downloadEnaERR("ERR2854359", tempdir)
    print(fnames)

    for fname in fnames:
        df=pd.DataFrame(data={
            "_filename":[fname],
            "_10xsampleid":["ERR2854359"]
        })

        util.smartmergeFilesFor10x(tempdir, df)

if __name__ == "__main__":
    main()


#E-MTAB-7316
#https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-7316/
#could be nice to start from PRJEB29298  sometimes
#https://www.ebi.ac.uk/ena/browser/view/ERR2854359

# e.g. #ftp.sra.ebi.ac.uk/vol1/fastq/SRR110/075/SRR11008275/SRR11008275_1.fastq.gz;ftp.sra.ebi.ac.uk/vol1/fastq/SRR110/075/SRR11008275/SRR11008275_2.fastq.gz


################################
# Given column _filename and _10xsampleid, figure out which files should be merged and/or converted to 10x-suitable format.
# Perform the ops and put them in the right place
#def smartmergeFilesFor10x(datasetdir, table):
#_filename, _10xsampleid


