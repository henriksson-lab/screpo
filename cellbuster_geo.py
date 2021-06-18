import requests
import sys
import pandas as pd
from io import StringIO
from tqdm import tqdm
import urllib
from pysradb import cli
import util
import GEOparse


def cellbuster_geo():
    gse = GEOparse.get_GEO(geo="GSE174786", destdir="./")

    gse.download_SRA("debojyoti.das@umu.se")
    gse.download_supplementary_files()


if __name__ == "__main__":
    cellbuster_geo()


