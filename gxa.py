import requests, zipfile, io
from os import listdir
from shutil import rmtree
from typing import List, Optional, NamedTuple

import util

################################
# Get the source IDs for a GXA entry - GSE* and SPR*
def getGXAsourceIDs(gxa_id: str) -> List[str]:

    #Download metadata zip, extract, and pull out the IDF file. Then clean up
    tmp = util.createSystemTempDir()
    r = requests.get("https://www.ebi.ac.uk/gxa/sc/experiment/"+gxa_id+"/download/zip?fileType=experiment-metadata&accessKey=")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(tmp)
    the_idf = tmp / [f for f in listdir(tmp) if ".idf.txt" in f][0]
    with the_idf.open() as f:
        content = f.readlines()
    rmtree(tmp, ignore_errors=True)

    #Get the source accessions.
    #Note that there is also Comment[SequenceDataURI], referring to SRR*, but these are not easy to deal with directly
    content=[x for x in content if x.startswith("Comment[SecondaryAccession]")][0]
    secondary_ids = content.strip().split("\t")
    secondary_ids.pop(0)

    return secondary_ids




################################
#for testing
def main():
    print(getGXAsourceIDs("E-GEOD-114530"))


if __name__ == "__main__":
    main()

