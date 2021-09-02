import os, shutil
import subprocess
from pysradb.sraweb import SRAweb
import config
import random
import string

################################
# If the id is not of type GSE*, try to convert it
def convertIDtoSRP(id: str):
    if id.startswith("SRP"):
        return id
    elif id.startswith("GSE"):
        sradb = SRAweb()
        id_srp = sradb.gse_to_srp(id)["study_accession"][0]
        return id_srp
    else:
        raise Exception("Don't know how to interpret ID "+id)


################################
# Download metadata
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


################################
# Move files to cellranger subdirectories ("samples")
def input_dir_tree(files, datasetid):

    datasetdir = config.getDatasetDir(datasetid)

    for file in files:
        file_parts = file.split("_")
        if len(file_parts) > 2:
            dir_name = '_'.join(file_parts[:2])
        else:
            dir_name = file_parts[0]

        todir = datasetdir / "samples" / dir_name
        todir.mkdir(parents=True, exist_ok=True)

        shutil.move(file,todir / file)


################################
# Download metadata and files from GEO
def download_geo(geo_id):

    # Create a new temporary directory
    conf = config.getCellbusterConfig()
    tempdir = config.getTempDir()
    tempdir = tempdir / (''.join(random.choice(string.ascii_lowercase) for i in range(20)))
    tempdir.mkdir(parents=True, exist_ok=True)

    print(tempdir)

    metadata = getCleanMetadataFromSRA(geo_id)

    outdir = str(list(set(metadata["study_accession"].tolist()))[0])
    run_id_list = metadata["run_accession"].tolist()
    print(outdir)
    print(run_id_list)

    # Download each file belonging to this GEO entry
    for run_id in run_id_list:


        #it appears that one better prefetch: prefetch SRR11816791 --max-size 100000000
        #some issues solved if done separately from the dump
        #this gives you in the folder: foo/foo.sra
        #then run fasterq-dump foo.sra --split-files --threads 16   and it will make your files

        command = "fasterq-dump " + "--split-files --threads 16 --outdir " + str(tempdir) + " " + run_id
        print(command)
        output = subprocess.call(command, cwd = tempdir, shell = True )
        print("exit status")
        print(output)
        if output == 0:
            command = "gzip " + str(tempdir) + "/*fastq"
            output = subprocess.call(command, cwd = tempdir, shell = True )
            print(command)

    files = os.listdir(tempdir)
    input_dir_tree(files, geo_id)



###########################################################
if __name__ == "__main__":
    # test GEO ID: "GSE126030"
    download_geo("GSE126030")
