import os, sys, re, shutil
import util
from fastqfileinfo import fastqinfo

# import pdb;pdb.set_trace()

def organizesampledir():
    tempdir = "/corgi/debojyoti/temp"

    files = [f for f in os.listdir(tempdir) if re.search('fastq.gz', f) or re.search('fq.gz',f)]
    for file in files:
        fileinfo = fastqinfo(tempdir + "/" + file)
        reqdirname = tempdir + "/" + fileinfo.id
        if not os.path.exists(reqdirname):
            os.makedirs(reqdirname)

        shutil.move(tempdir + "/" + file, reqdirname)



if __name__ == "__main__":
    organizesampledir()
