

#https://www.ebi.ac.uk/arrayexpress/help/programmatic_access.html


import requests

r = requests.get('https://www.ebi.ac.uk/arrayexpress/json/v3/files/E-MTAB-7316')
dat = r.json()

print(dat)





#what files there are:
#https://www.ebi.ac.uk/arrayexpress/experiments/E-MTAB-7316/files/


#metadata:
#https://www.ebi.ac.uk/arrayexpress/files/E-MTAB-7316/E-MTAB-7316.sdrf.txt

#### can extract these 
#Comment[read1 file]	
#Comment[read2 file]
#Comment[index1 file]
### for some crazy reason there is FASTQ_URI after each comment... non-unique column




#wish to extract all the metadata into a format we can load into a nice Pandas df later!
