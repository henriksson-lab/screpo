CellBuster - a framework for single-cell raw data retrieval and reprocessing
============================================================================

Do you want to reanalyze some previous single-cell data? Is the data in a database
that requires a weird download tool? Is the data in an inconsistent format?
Who you gonna call.......?

==Supported databases==

* EBI ArrayExpress
* EBI GXA
* NCBI GEO
* NCBI SRA
* Human Cell Atlas (HCA)
* European Genome-phenome Archive (EGA)  [wip]

Only 10x datasets can be retrieved as of now; other single cell datasets are
too non-standardized to be within the scope of this tool.


==Installation==

Note that you need to configure sra toolkit before you can download any files from SRA.
One particular concern is the location of the cache. Put this on a disk that is large and fast.
This can be configured with the following command, that must be run at least once:

vdb-config -i

Next, you need to decide where you want to store all datasets downloaded by this tool. Copy
the file template_cellbuster.json to ~/.cellbuster.json or ./cellbuster.json; you can then
edit it to set the repository location. This file also has other settings worth checking out.
In particular, set the temp directory to a large and fast disk.

Overall advice on cache and temp directories: It is beneficial for performance if these are
NOT the disk where you keep the single cell data in the end. By keeping them separate, you
can read from one place, and write to another - twice the performance!


==Dependencies==

Key other packages used are:

https://anaconda.org/bioconda/sra-tools -- SRA toolkit


==TODO==




==License==

See https://opensource.org/licenses/BSD-2-Clause


==Authors==

* Johan Henriksson
* Debojyoti Das

==Cite==

Not required but much appreciated! It motivates us to keep developing tools like this one:

TODO


A quick guide to database IDs
=============================

This table might help you navigate the way-too-many accession systems out there

== GEO namespace ==
GSE*    An expression dataset such as https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114530
GSM*

== SRA namespace ==
SRP*    A sequencing project, https://www.ncbi.nlm.nih.gov/sra?term=SRP147554
SRX*    An experiment, corresponds to GSM*,  https://www.ncbi.nlm.nih.gov/sra/SRX5126514[accn]
SRR*    A sequencing run
SRS*    A sample

== Bioproject ==
PRJNA*  https://www.ncbi.nlm.nih.gov/bioproject/PRJNA471694
SAMN*   corresponds to SRS*

