import requests
import sys
import pandas as pd
from io import StringIO


def listAE():
    #note: datasets E-CURD  , E-GEOD, E-HCAD,  are not directly from AE. should we support the HCA?
    r = requests.get('https://www.ebi.ac.uk/gxa/sc/json/experiments')
    dat = r.json()

    set_10x_tech=set(["10x5prime","10xv2","10xv3"])

    for exp in dat["experiments"]:
        expid=exp["experimentAccession"]
        expdesc=exp["experimentDescription"]
        cellcount=exp["numberOfAssays"]

        #Only look at human for now
        if exp["species"]=="Homo sapiens":

            #Only consider 10x technologies
            if len(set_10x_tech.intersection(set(exp["technologyType"])))>0:
                print(expid+"\t\t"+str(cellcount)+"\t\t "+expdesc)

#try out: E-MTAB-7316
def getmetaAE(datasetid):

    r = requests.get('https://www.ebi.ac.uk/arrayexpress/json/v3/files/E-MTAB-7316')
    dat = r.json()

    filemeta="https://www.ebi.ac.uk/arrayexpress/files/"+datasetid+"/"+datasetid+".sdrf.txt"
    r = requests.get(filemeta).content.decode('utf-8')
    df = pd.read_csv(StringIO(r), sep="\t")
    print(df)
    print(df.columns)

    df['Comment[read1 file]', 'Comment[FASTQ_URI]'

#what files there are:
#https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-7316/files/
#https://www.ebi.ac.uk/arrayexpress/files/E-MTAB-7316/E-MTAB-7316.sdrf.txt

#### can extract these 
#Comment[read1 file]    
#Comment[read2 file]
#Comment[index1 file]
### for some crazy reason there is FASTQ_URI after each comment... non-unique column


def download(datasetid):
    getmetaAE(datasetid)


def printHelp():
    print("""
  CellBuster - a framework for single-cell raw data retrieval and reprocessing
  ============================================================================

  update              Update the list of available datasets (not sure if needed)

  listdownloads       List possible datasets to download

  download DATASET    Download a dataset


""")




def listDownloads():
        listAE()



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

