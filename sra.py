import os, shutil
import subprocess
from pysradb.sraweb import SRAweb
import config


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

def input_dir_tree(files):

    for file in files:
        dir_name = '_'.join(file.split("_")[:2])

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        shutil.move(file,dir_name + "/" + file)


def download_geo(geo_id):

    conf = config.getCellbusterConfig()
    tempdir = str(config.getTempDir())

    print(tempdir)

    metadata = getCleanMetadataFromSRA(geo_id)


    outdir = str(list(set(metadata["study_accession"].tolist()))[0])
    run_id_list = metadata["run_accession"].tolist()
    print(outdir)
    print(run_id_list)


    for run_id in run_id_list:

        command = "fasterq-dump " + "--split-files --threads 16 --outdir " + tempdir + " " + run_id
        print(command)
        output = subprocess.call(command, cwd = tempdir + "/..", shell = True )
        print("exit status")
        print(output)
        if output == 0:
            command = "gzip " + tempdir + "/*fastq"
            output = subprocess.call(command, cwd = tempdir + "/..", shell = True )
            print(command)

    files = os.listdir(tempdir)
    input_dir_tree(files)

if __name__ == "__main__":
    # test GEO ID: "GSE126030"
    download_geo("GSE126030")
