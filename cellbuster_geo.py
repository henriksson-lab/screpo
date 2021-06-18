import os, sys
import GEOparse
import pysradb

from pysradb.sraweb import SRAweb
from pysradb.geodb import GEOdb
from pysradb.search import GeoSearch


def cellbuster_geo():
#    gse = GEOparse.get_GEO(geo="GSE158984", destdir="./")
#    gse = GEOparse.get_GEO(geo="GSE1563", destdir="./")

    db = GeoSearch(accession = "GSE57249")
    import pdb;pdb.set_trace()
    df_metadata = db.geo_metadata('GSE57249', detailed=True)
    list=df_metadata["run_accession"].tolist()
    
#    gse.download_SRA("debojyoti.das@umu.se", nproc=16)
#    gse.download_supplementary_files()
    for i in list:
        print(i)

    print(" Download complete!!")


if __name__ == "__main__":
    cellbuster_geo()


