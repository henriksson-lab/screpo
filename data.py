import config
import pandas as pd
import scanpy as sc


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


################################
# Get a path to the count file, .h5d
def getDatasetAnndata(datasetid):
    ds = config.getDatasetDir(datasetid)
    print("TODO")
    list_adata = []
    for fname in ds.iterdir():
        adata = sc.read_10x_h5(str(ds / fname / "outs" / "filtered_feature_bc_matrix.h5"))
        list_adata.append(adata)
        #TODO should load the metadata and attach it
    return list_adata


#For testing
def main():
    print(666)
    #downloadCanogamez()
    #print(getCellbusterConfig())
    #downloadEGA("EGAF00002554994")
    #print(readDatasetMeta("canogamez"))

if __name__ == "__main__":
    main()

