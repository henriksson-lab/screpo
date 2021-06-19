import requests
import json
from typing import List, Optional, Tuple, NamedTuple

import util

################################################################
#
# How the API works;
# Overall hierarchy: Project => Samples => Files
#
# https://data.humancellatlas.org/apis
# https://service.azul.data.humancellatlas.org/#/Index/get_index_projects__project_id_
# https://github.com/DataBiosphere/azul/blob/develop/docs/download-project-matrices.ipynb
# https://data.humancellatlas.org/metadata/dictionary/file/sequence_file
################################################################



#available files
#https://data.humancellatlas.org/explore/files?filter=%5B%7B%22facetName%22:%22specimenOrgan%22,%22terms%22:%5B%22blood%22%5D%7D,%7B%22facetName%22:%22projectId%22,%22terms%22:%5B%224a95101c-9ffc-4f30-a809-f04518a23803%22%5D%7D%5D


################################
# Map from cellbuster ID to HCA id
def toHCAprojid(project_uuid: str):
    if "HCA-" in project_uuid:
        project_uuid = project_uuid.replace("HCA-")
    return project_uuid


################################
# Get the metadata for a project
def getProjectMeta(project_uuid: str):
    project_uuid = toHCAprojid(project_uuid)
    endpoint_url = f'https://service.azul.data.humancellatlas.org/index/projects/{project_uuid}'
    r = requests.get(endpoint_url)  # could check that the response code is 200
    dat = r.json()
    return dat

#getProjectMeta('005d611a-14d5-4fbf-846e-571a1f874f70')
#has raw files for certain:
#getProjectMeta('4a95101c-9ffc-4f30-a809-f04518a23803') #https://data.humancellatlas.org/explore/projects/4a95101c-9ffc-4f30-a809-f04518a23803
#https://data.humancellatlas.org/explore/projects?filter=%5B%7B%22facetName%22:%22specimenOrgan%22,%22terms%22:%5B%22blood%22%5D%7D,%7B%22facetName%22:%22projectId%22,%22terms%22:%5B%224a95101c-9ffc-4f30-a809-f04518a23803%22%5D%7D%5D


################################
# Get list of files for a given project ID
def getFileListForProject(project_uuid: str) -> List[Tuple[str, str]]:
    project_uuid = toHCAprojid(project_uuid)

    # Perform the REST query
    r = requests.get('https://service.azul.data.humancellatlas.org/index/files', params={
        "filters":json.dumps({
            "projectId": {
                "is": [project_uuid]
            }
        }),
        "size":"1000",  # virtually infinite
        "sort":"fileName",
        "order":"asc"
    })
    dat = r.json()

    # Extract files from all "hits"
    list_files = []
    for hit in dat["hits"]:
        list_files = list_files + hit["files"]

    # Obtain list of raw data files. These are normally fastq.gz it seems.
    # Only return (file name, URL)
    list_files = [f for f in list_files if "DNA sequence (raw)" in f["content_description"]]
    list_files = [(f["name"], f["url"]) for f in list_files]
    return list_files






################################
# Get the list of projects
def getListProjects():
    # Request the metadata
    r = requests.get('https://service.azul.data.humancellatlas.org/index/projects', params={
            "filters":json.dumps({
            }),
            "size":"1000",  # virtually infinite
            "sort":"projectId",
            "order":"asc"
        })
    dat = r.json()

    # For each project, pull out the relevant info
    list_projects = []
    for h in dat["hits"]:
        # What would be call this project?
        projid = "HCA-"+h["entryId"]

        # Get a list of protocols used
        list_protocols = util.flatten([prot["libraryConstructionApproach"] for prot in h["protocols"] if "libraryConstructionApproach" in prot])

        # Figure out what title to designate this dataset; it can be in multiple?
        list_titles=[p["projectTitle"] for p in h["projects"]]
        if len(list_titles)>0:
            title=list_titles[0]
        else:
            title=""

        list_projects.append({
            "id":projid,
            "title":title,
            "protocols":list_protocols
        })
    return list_projects


def printListProjects():
    for p in getListProjects():
        print(p["id"] + "\t" + p["title"] + " ("+",".join(p["protocols"])+")")




#getProjectMeta("4a95101c-9ffc-4f30-a809-f04518a23803")

#util.prettyPrintJSON(dat)




#printListProjects()








################################
# Container of all functions related to AE
class LoaderHCA:
    def __init__(self, datasetid, desc):
        self.datasetid=datasetid
        self.desc=desc

    def download(self):
        print(666)
        #downloadAE(self.datasetid)


################################
# Figure out what datasets can be downloaded
def populateListOfDatasets(list_of_datasets):
    for p in getListProjects():
        if any(["10X" in protname for protname in p["protocols"]]):
            list_of_datasets[p["id"]] = LoaderHCA(p["id"], p["title"] + " ("+",".join(p["protocols"])+")")
