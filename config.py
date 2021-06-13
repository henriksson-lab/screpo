import os
import json
from pathlib import Path

################################
#The config file is either in the current directory, or HOME
def getCellbusterConfig():
    p=Path(".") / "cellbuster.json"
    if p.is_file():
        with open(p) as f:
            return json.load(f)
    HOME = os.getenv('HOME')
    if not HOME is None:
        p=Path(HOME) / ".cellbuster.json"
        if p.is_file():
            with open(p) as f:
                return json.load(f)
    return {
        "localrepo":"./repo"
    }


################################
#Get directory for a dataset
def getDatasetDir(datasetid):
    conf = getCellbusterConfig()
    return Path(conf["localrepo"]) / datasetid


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
# Get a path to the count file, .h5d
def getDatasetCounts(datasetid):
    print(666)




#For testing
def main():
    #print(getCellbusterConfig())
    print(getDatasetConfig("E-MTAB-7316"))

if __name__ == "__main__":
    main()
