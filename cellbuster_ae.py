import requests
import sys
import pandas as pd
from io import StringIO


import data
import util
import config

################################
# Download one dataset from ArrayExpress
def downloadAE(datasetid: str):

    datasetdir = config.getDatasetDir(datasetid)

    r = requests.get('https://www.ebi.ac.uk/arrayexpress/json/v3/files/E-MTAB-7316')
    dat = r.json()

    filemeta="https://www.ebi.ac.uk/arrayexpress/files/"+datasetid+"/"+datasetid+".sdrf.txt"
    r = requests.get(filemeta).content.decode('utf-8')
    df = pd.read_csv(StringIO(r), sep="\t")

    #Remove columns with metadata likely not of interest
    def keepColumn(c: str):
        listBadCol = ["URI","file","File","NOMINAL_SDEV", "NOMINAL_LENGTH","Performer","Protocol REF",
                      "LIBRARY_LAYOUT", "LIBRARY_SELECTION", "LIBRARY_SOURCE","LIBRARY_STRAND",
                      "Technology Type","SPOT_LENGTH","barcode","cDNA","umi","ENA_","Scan Name","primer",
                      "single cell isolation","BioSD_SAMPLE","input molecule","end bias","Material Type","cell number"]
        return not any([x in c for x in listBadCol])

    #Rename columns to something sensible. foo[x] => x
    def cleanColumnName(c: str):
        if "]" in c:
            return c.split("[")[1].split("]")[0]
        else:
            return c

    print(df)

    #Clean up metadata
    subcond = df[[x for x in df.columns if keepColumn(x)]]
    subcond = subcond.rename(cleanColumnName, axis='columns')
    print(subcond)

    #Write metadata
    #data.writeDatasetMeta(datasetid, df)
    #data.writeDatasetMeta(datasetid, subcond)
    subcond=cond[["experimental_condition","cell_type","time_point"]].copy()
    subcond["_10xsampleid"] = cond["sample_id"]
    subcond_red=subcond.drop_duplicates()
    data.writeDatasetMeta(datasetid, subcond_red)

    list_sampleid = df["Source Name"]


    list_file_r1=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[read1 file]'].tolist()]
    list_file_r2=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[read2 file]'].tolist()]
    list_file_i1=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[index1 file]'].tolist()]

    #if we download from ENA, can learn from here:
    #https://github.com/ebi-gene-expression-group/atlas-fastq-provider/blob/develop/atlas-fastq-provider-functions.sh

    for i in range(0,len(df.index)):
        print(i)
        #download_one10x("tofolder", list_file_r1[i], list_file_r2[i], list_file_i1[i])

        s=list_sampleid[i]
        dir10x = datasetdir / "rawfq"
        path_r1 = dir10x / s / (s+"_S1_L001_R1_001.fastq.gz")
        path_r2 = dir10x / s / (s+"_S1_L001_R2_001.fastq.gz")
        (dir10x / s).mkdir(parents=True,exist_ok=True)

        util.download_url(list_file_r1[i], path_r1)
        util.download_url(list_file_r2[i], path_r2)

        #TODO but what to do if there are multiple files per sample? multiple lanes?




################################
#
#def download_one10x(tofolder, file_r1, file_r2, file_i1):
#    print(file_r1)
#    util.download_url(file_r1, "/tmp/test")

#what files there are:
#https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-7316/files/
#https://www.ebi.ac.uk/arrayexpress/files/E-MTAB-7316/E-MTAB-7316.sdrf.txt



################################
# Container of all functions related to AE
class LoaderAE:
    def __init__(self, datasetid, desc):
        self.datasetid=datasetid
        self.desc=desc

    def download(self):
        downloadAE(self.datasetid)



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
                list_of_datasets[expid]=LoaderAE(expid,expdesc+" ("+exp["species"]+","+str(cellcount)+")")



#for testing
def main():
    util.fake_download=True
    downloadAE("E-MTAB-7316")

if __name__ == "__main__":
    main()



#ERS2852886   for a sample... wut?
