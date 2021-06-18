import config
import pandas as pd

################################
# Read the sample meta for a dataset
def readDatasetMeta(datasetid):
    ds = config.getDatasetDir(datasetid)
    p = ds / "samplemeta.csv"
    return pd.read_csv(p)

################################
# Write the sample meta for a dataset
def writeDatasetMeta(datasetid, dat):
    ds = config.getDatasetDir(datasetid)
    ds.mkdir(parents=True,exist_ok=True)
    dat.to_csv(ds / "samplemeta.csv", index=False)

################################
# Write a special dataframe for a dataset
def writeDatasetDF(datasetid, dat, filename: str):
    ds = config.getDatasetDir(datasetid)
    ds.mkdir(parents=True,exist_ok=True)
    dat.to_csv(ds / filename, index=False)



#For testing
def main():
    print(666)
    #downloadCanogamez()
    #print(getCellbusterConfig())
    #downloadEGA("EGAF00002554994")
    #print(readDatasetMeta("canogamez"))

if __name__ == "__main__":
    main()

