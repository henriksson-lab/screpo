import os
import json
from pathlib import Path

################################
#The config file is either in the current directory, or HOME
def getCellbusterConfig():
    #First check the home folder
    HOME = os.getenv('HOME')
    if not HOME is None:
        p=Path(HOME) / ".cellbuster.json"
        if p.is_file():
            with open(p) as f:
                return json.load(f)
    #Check current directory as secondary
    p=Path(".") / "cellbuster.json"
    if p.is_file():
        with open(p) as f:
            return json.load(f)
    return {
        "localrepo":"./repo",
        "tempdir":"./temp"
    }


################################
#Get directory for a dataset
def getDatasetDir(datasetid):
    conf = getCellbusterConfig()
    return Path(conf["localrepo"]) / datasetid


################################
#Get temporary directory
def getTempDir():
    conf = getCellbusterConfig()
    tempdir = Path(conf["tempdir"])
    tempdir.mkdir(parents=True, exist_ok=True)
    return tempdir

################################
# Get settings for a single dataset... can also all sorts of stuff, like download status
def getDatasetConfig(datasetid):
    ds = getDatasetDir(datasetid)
    p = ds / "dataset.cb"
    if p.is_file():
        with open(p) as f:
            return json.load(f)

################################
#Settings for a single dataset... can also all sorts of stuff, like download status
def setDatasetConfig(datasetid, configdata):
    ds = getDatasetDir(datasetid)
    ds.mkdir(parents=True,exists_ok=True)
    p = ds / "dataset.cb"
    with p.open('w', encoding='utf-8') as f:
        json.dump(configdata, f, ensure_ascii=False, indent=4)











################################
#For testing
def main():
    #print(getCellbusterConfig())
    print(getDatasetConfig("E-MTAB-7316"))

if __name__ == "__main__":
    main()
