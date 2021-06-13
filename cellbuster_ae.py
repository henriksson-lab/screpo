import requests
import sys
import pandas as pd
from io import StringIO
from tqdm import tqdm
import urllib


import util


################################
#try out: E-MTAB-7316
def getmetaAE(datasetid):

    r = requests.get('https://www.ebi.ac.uk/arrayexpress/json/v3/files/E-MTAB-7316')
    dat = r.json()

    filemeta="https://www.ebi.ac.uk/arrayexpress/files/"+datasetid+"/"+datasetid+".sdrf.txt"
    r = requests.get(filemeta).content.decode('utf-8')
    df = pd.read_csv(StringIO(r), sep="\t")
    print(df)
    print(df.columns)

    list_file_r1=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[read1 file]'].tolist()]
    list_file_r2=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[read2 file]'].tolist()]
    list_file_i1=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[index1 file]'].tolist()]

    for i in range(0,len(df.index)):
        print(i)
        download_one10x("tofolder", list_file_r1[i], list_file_r2[i], list_file_i1[i])


################################
#
def download_one10x(tofolder, file_r1, file_r2, file_i1):
    print(file_r1)
    util.download_url(file_r1, "/tmp/test")

#what files there are:
#https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-7316/files/
#https://www.ebi.ac.uk/arrayexpress/files/E-MTAB-7316/E-MTAB-7316.sdrf.txt

#### can extract these 
#Comment[read1 file]    
#Comment[read2 file]
#Comment[index1 file]
### for some crazy reason there is FASTQ_URI after each comment... non-unique column





################################
# Container of all functions related to AE
class LoaderAE:
    def __init__(self, datasetid, desc):
        self.datasetid=datasetid
        self.desc=desc

    def download(self):
        getmetaAE(self.datasetid)



################################
# Figure out what datasets can be downloaded
def populateListOfDatasets(list_of_datasets):
    #note: datasets E-CURD  , E-GEOD, E-HCAD,  are not directly from AE. should we support the HCA?
    r = requests.get('https://www.ebi.ac.uk/gxa/sc/json/experiments')
    dat = r.json()

    set_10x_tech=set(["10x5prime","10xv2","10xv3"])

    for exp in dat["experiments"]:
        expid=exp["experimentAccession"]
        expdesc=exp["experimentDescription"]
        cellcount=exp["numberOfAssays"]

        #Only look at human for now. Also need to be MTAB
        if exp["species"]=="Homo sapiens" and "E-MTAB" in expid:

            #Only consider 10x technologies
            if len(set_10x_tech.intersection(set(exp["technologyType"])))>0:
                #print(expid+"\t\t"+str(cellcount)+"\t\t "+expdesc)
                list_of_datasets[expid]=LoaderAE(expid,expdesc+" ("+str(cellcount)+")")



#for testing
def main():
    print(666)
    getmetaAE("E-MTAB-7316")

if __name__ == "__main__":
    main()


