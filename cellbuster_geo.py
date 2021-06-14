import requests
import sys
import pandas as pd
from io import StringIO
from tqdm import tqdm
import urllib
from pysradb import cli
import util


#for testing
def main():
    print(666)
    cli.parse_args("metadata GSE174786")

if __name__ == "__main__":
    main()


