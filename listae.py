import requests

r = requests.get('https://www.ebi.ac.uk/gxa/sc/json/experiments')
dat = r.json()

set_10x_tech=set(["10x5prime","10xv2","10xv3"])

for exp in dat["experiments"]:
	expid=exp["experimentAccession"]
	expdesc=exp["experimentAccession"]

	#Only look at human for now
	if exp["species"]=="Homo sapiens":

		#Only consider 10x technologies
		if len(set_10x_tech.intersection(set(exp["technologyType"])))>0:
			print(exp)



#print(r.json())
