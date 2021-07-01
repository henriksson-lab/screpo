from typing import List, Optional, NamedTuple
import config
import subprocess



################################
# Upload the data to arrayexpress (annotare)
def uploadArrayExpress(datasetid: str, uploadname: str):
    datasetdir = config.getDatasetDir(datasetid)



    # Collect list of all samples
    list_files=[]
    #glob  samples/*/*/*.fq.gz

    subprocess.call(["ascp", "-P", "33001"]+list_files+["aexpress@fasp.ebi.ac.uk:"+uploadname], shell=True)



    # Produce MD5 sums of the files. Could do this lazily and place in files as *.md5?
    # print fname md5sum
