import subprocess
import pandas as pd
from pathlib import Path

import config
import data
import util


################################
# Download the data
def downloadCanogamez():
    datasetid = "canogamez2020"
    datasetdir = config.getDatasetDir(datasetid)

    #Load metadata that isn't broken (it is at EGA)
    cond=pd.read_csv("newmeta/canogamez.csv",delimiter="\t")

    #Clean up and store the metadata
    subcond=cond[["experimental_condition","cell_type","time_point"]].copy()
    subcond["_10xsampleid"] = cond["sample_id"]
    subcond_red=subcond.drop_duplicates()
    data.writeDatasetMeta(datasetid, subcond_red)

    #Merge files as needed
    subcond["_filename"] = cond["file_name"]
    util.smartmergeFilesFor10x(datasetdir, subcond[["_filename","_10xsampleid"]])



################################
# Class with custom operations for this particular dataset
class EddieGomez2020:
    datasetid = "canogomez2020"
    desc = "Cano-Gomez 2020 T cell effectorness"
    def download(self):
        downloadCanogamez()




#### somehow this instance should be sent to main...
object2givetomain = EddieGomez2020()



#For testing
def main():
    #print(666)
    downloadCanogamez()
    #print(getCellbusterConfig())
    #downloadEGA("EGAF00002554994")
    print(data.readDatasetMeta("canogamez"))

if __name__ == "__main__":
    main()






#sample_id   #use for 10x output
#donor_id
#experimental_condition
#cell_type

#originally, this would be the structure:
#EGA_id  /   file_name



