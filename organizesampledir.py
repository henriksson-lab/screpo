import os, sys, re, shutil
import pandas as pd
import util
from fastqfileinfo import fastqinfo


def organizesampledir():

    tempdir = "/corgi/debojyoti/temp"

    files = [f for f in os.listdir(tempdir) if re.search('fastq.gz', f) or re.search('fq.gz',f) or re.search('fastq', f) or re.search('fq', f)]


    samples = []

    for file in files:

        fileinfo = fastqinfo(tempdir + "/" + file)
        reqdirname = tempdir + "/" + fileinfo.id

        samples.append(fileinfo.id)

        if not os.path.exists(reqdirname):
            os.makedirs(reqdirname)

        shutil.move(tempdir + "/" + file, reqdirname)

    samples = list(set(samples))

    for i, sample in enumerate(samples):


        files = os.listdir(tempdir + "/" + sample)

        read_lengths = [fastqinfo(tempdir + "/" + sample + "/" + f).description.split("length=")[-1] for f in files]
            
        table = pd.DataFrame({"file": files, "read_length": read_lengths})

        table.sort_values(by = ["read_length"], inplace = True)

        renamed_file = []

        rows = table.shape[0]

        if rows == 1 or rows == 2:
            lanes = 1
        else:
            lanes = rows/3

        lane = 1

        for ifname, fname in enumerate(table["file"].tolist()):
            if lanes == 1:
                lane = 1
            else:
                if ifname % 3 == 0:
                    lane = lane + 1


            if rows == 2:
                if ifname == 0:
                    renamed_file.append(fname.split("_")[0] + "_S1_L00" + str(lane) + "_R1_001.fastq.gz") 
                else:
                    renamed_file.append(fname.split("_")[0] + "_S1_L00" + str(lane) + "_R2_001.fastq.gz") 
            elif rows % 3 == 0:
                if ifname < lanes:
                    renamed_file.append(fname.split("_")[0] + "_S1_L00" + str(lane) + "_I1_001.fastq.gz") 
                elif ifname >= lanes and ifname <= lanes+1:
                    renamed_file.append(fname.split("_")[0] + "_S1_L00" + str(lane) + "_R1_001.fastq.gz") 
                else:
                    renamed_file.append(fname.split("_")[0] + "_S1_L00" + str(lane) + "_R2_001.fastq.gz") 
            else:
                    renamed_file.append(fname.split("_")[0] + "_S1_L00" + str(lane) + "_R1_001.fastq.gz") 

                

        table["renamed_file"] = renamed_file

        for row in range(table.shape[0]):
            shutil.move(tempdir + "/" + sample + "/" + table["file"].values[row], tempdir + "/" + sample + "/" + table["renamed_file"].values[row])




if __name__ == "__main__":
    organizesampledir()
