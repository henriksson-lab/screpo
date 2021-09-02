import requests
import sys
# import pandas as pd
import GEOparse
import multiprocessing
import pyrpipe


nproc=multiprocessing.cpu_count()

def cellbuster_geo():
    gse = GEOparse.get_GEO(geo="GSE158984", destdir="./")

    
    sra = pyrpipe.sra.SRA(gse.get_accession())
    import pdb; pdb.set_trace()
    
    if sra:
        gse.download_SRA("debojyoti.das@umu.se", nproc = nproc/2)

    gse.download_supplementary_files()
    print(" Download complete!!")


if __name__ == "__main__":
    cellbuster_geo()
