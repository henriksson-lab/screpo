import requests, zipfile, io
import os
from tempfile import gettempdir
from pathlib import Path
from shutil import rmtree


gxa_id="E-GEOD-114530"


#Create a temp dir
tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
os.makedirs(tmp)

#Download
r = requests.get("https://www.ebi.ac.uk/gxa/sc/experiment/"+gxa_id+"/download/zip?fileType=experiment-metadata&accessKey=")
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(tmp)

print(tmp)

Path(tmp) /

#Clean up files
#rmtree(tmp, ignore_errors=True)


#Search for a line, like:
#Comment[SecondaryAccession]	GSE114530	SRP147554