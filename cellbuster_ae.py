import requests
import pandas as pd
from io import StringIO

import data
import util
import config
import ena

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

    data.writeDatasetDF(datasetid, df, "samplemeta.csv.ae")
    print(df)

    #Write metadata
    #data.writeDatasetMeta(datasetid, df)
    #data.writeDatasetMeta(datasetid, subcond)
    subcond = df[[x for x in df.columns if keepColumn(x)]]
    subcond = subcond.rename(cleanColumnName, axis='columns')
    #subcond=cond[["experimental_condition","cell_type","time_point"]].copy()
    #subcond["_10xsampleid"] = subcond["sample_id"]
    subcond_red=subcond.drop_duplicates()
    data.writeDatasetMeta(datasetid, subcond_red)

    #Clean up metadata
    print(subcond)


    #Download the files
    ena_samples = df['Comment[ENA_SAMPLE]']  #ERR records that we want
    list_sampleid = df["Source Name"]
    tempdir = util.getTempDir()
    for i in range(0,len(df.index)):
        fname = ena.downloadEnaERR(ena_samples[i], tempdir)
        print(fname)
        df = pd.DataFrame(data={
            "_filename": [fname],
            "_10xsampleid": [list_sampleid[i]})
        util.smartmergeFilesFor10x(tempdir, df)
        #TODO this does not use the fact that there may be multiple files



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
