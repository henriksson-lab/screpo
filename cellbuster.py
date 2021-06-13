import requests
import sys
import pandas as pd
from io import StringIO
from tqdm import tqdm
import urllib

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)
def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)





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

    list_file_r1=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[read1 file]'].tolist()]
    list_file_r2=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[read2 file]'].tolist()]
    list_file_i1=['ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/'+datasetid+'/'+x for x in df['Comment[index1 file]'].tolist()]

    for i in range(0,len(df.index)):
        print(i)
        download_one10x("tofolder", list_file_r1[i], list_file_r2[i], list_file_i1[i])



def download_one10x(tofolder, file_r1, file_r2, file_i1):
    print(file_r1)
    download_url(file_r1, "/tmp/test")

#what files there are:
#https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-7316/files/
#https://www.ebi.ac.uk/arrayexpress/files/E-MTAB-7316/E-MTAB-7316.sdrf.txt

#### can extract these 
#Comment[read1 file]    
#Comment[read2 file]
#Comment[index1 file]
### for some crazy reason there is FASTQ_URI after each comment... non-unique column

def runCellRanger(datasetid,localcores=8,expectcells=5000):
    #run cellranger on a locally existing dataset
    print("foo")

def download(datasetid):
    getmetaAE(datasetid)


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

