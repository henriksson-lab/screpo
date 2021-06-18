from pysradb.sraweb import SRAweb

def prefetch(ids, outdir):
    subprocess.call(["prefetch", "--output-directory", outdir]+ids, shell=True)

def fasterqDumpSplit():
    subprocess.call(["fasterq-dump", "--output-directory", outdir]+ids, shell=True)

def prefetch(ids, outdir):
    subprocess.call(["prefetch", "--output-directory", outdir]+ids, shell=True)

def convertIDtoSRP(id: str):
    if id.startswith("SRP"):
        return id
    elif id.startswith("GSE"):
        sradb = SRAweb()
        id_srp = sradb.gse_to_srp(id)["study_accession"][0]
        return id_srp
    else:
        raise Exception("Don't know how to interpret ID "+id)

def getCleanMetadataFromSRA(id: str):
    id_srp = convertIDtoSRP(id)
    sradb = SRAweb()
    df = sradb.sra_metadata(id_srp, detailed=True)
    # Remove columns with metadata likely not of interest
    def keepColumn(c: str):
        listBadCol = ["sra_url","ena_fastq","total_","run_alias"]
        return not any([x in c for x in listBadCol])
    # Remove columns that just contain NA
    subcond = df[[x for x in df.columns if not df[x].isnull().all()]]
    subcond = subcond[[x for x in subcond.columns if keepColumn(x)]]
    return subcond



#For testing
def main():
    #print(getCellbusterConfig())
    getCleanMetadataFromSRA("GSE171273")

if __name__ == "__main__":
    main()


