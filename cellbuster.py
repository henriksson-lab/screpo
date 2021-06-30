import re

import requests
import sys
import pandas as pd
from io import StringIO
from tqdm import tqdm
import urllib


################################
# Dataset managers. Later on we should move to a proper plugin system
import cellbuster_canogamez2020
import cellbuster_ae
import cellbuster_hca
import re
import sra


################################
# List of all datasets.
# AE datasets are lazily loaded to prevent more network traffic than needed
list_of_datasets = {
    "cellbuster_canogamez2020":cellbuster_canogamez2020.object2givetomain
}

def lazyloadDatasets():
    cellbuster_ae.populateListOfDatasets(list_of_datasets)
    cellbuster_hca.populateListOfDatasets(list_of_datasets)

################################
# Should likely be moved
def runCellRanger(datasetid,localcores=8,expectcells=5000):
    #run cellranger on a locally existing dataset
    print("foo")


################################
# Download a dataset
def download(datasetid):
    if re.search('^G', datasetid, re.IGNORECASE):
        sra.download_geo(datasetid)
    else:
        lazyloadDatasets()
        list_of_datasets[datasetid].download()


################################
# Generate a list of possible downloads
def listDownloads():
    lazyloadDatasets()
    for ds in list_of_datasets.values():
        print(ds.datasetid+"\t\t"+ds.desc)


################################
# Print help to screen
def printHelp():
    print("""
  CellBuster - a framework for single-cell raw data retrieval and reprocessing
  ============================================================================

  update                 Update the list of available datasets (not sure if needed)

  listdownloads          List possible datasets to download

  listlocal              List locally available datasets

  push SERVER DATASET    Push a dataset to a remote reposity.
  pull SERVER DATASET    Pull a dataset from a remote reposity.
  pushall SERVER
  pullall SERVER
                         SERVER is in scp format, user@server:/pathtodir

  download DATASET       Download a dataset
""")




################################
# Main command line interface
def main():
    #could consider https://docs.python.org/3/library/argparse.html
    if len(sys.argv)==1:
        printHelp()
    elif sys.argv[1]=="listdownloads":
        listDownloads()
    elif sys.argv[1]=="download" and len(sys.argv)==3:
        download(sys.argv[2])
    else:
        print("Invalid: "+sys.argv[1])
        printHelp()

if __name__ == "__main__":
    main()

