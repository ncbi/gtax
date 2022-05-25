GTax
====

**GTax** python package provides tools for the creation of the GTax sequence-based database. This database includes
one assembly per organism deposited in the NCBI Genomes database. The sequences are organized by 19 taxonomic levels
from *superkindom* to *clades*. Python pickle files are also provided with a graph data structure for the taxonomic 
tree.

Read the Docs at: https://gtax.readthedocs.io/

Current version
---------------

The current public version is available in GCP for download. You need to use your GCP project as this bucket uses 
**Requester Pays** option.

```
gsutil -u <you-GCP-project> -m cp -r gs://gtax-database/20211025 .
```
    
The database is comprised of two folder: **blastdb** and **fasta**. The **blastdb** folder include the BLAST 
indexes for BLAST searches. The **fasta** folder includes the FASTA files for the taxonomy groups and two 
Python Objects in pickle files (**taxonomy.pickle** and **taxonomy_groups.pickle**) which are used to load
all GTax metadata into the [Taxonomy class](https://github.com/ncbi/gtax/blob/main/src/gtax/taxonomy.py#L37)

```python
from gtax.taxonomy import Taxonomy
taxonomy = Taxonomy(tax_pickle_file='taxonomy.pickle', group_pickle_file = 'taxonomy_groups.pickle')
```
Output:

```text
2374509 taxonomies loaded
bacteria Node: 526449 Sequences: 16137
archaea Node: 13927 Sequences: 554
liliopsida Node: 46167 Sequences: 265
eudicotyledons Node: 145896 Sequences: 880
viridiplantae Node: 45954 Sequences: 184
fungi Node: 179151 Sequences: 797
arthropoda Node: 883534 Sequences: 1364
neoteleostei Node: 29373 Sequences: 1437
actinopterygii Node: 20735 Sequences: 1047
glires Node: 5236 Sequences: 2178
primates Node: 1019 Sequences: 433
carnivora Node: 761 Sequences: 286
artiodactyla Node: 1184 Sequences: 447
amphibia Node: 12268 Sequences: 122
sauropsida Node: 31218 Sequences: 1073
sarcopterygii Node: 4759 Sequences: 229
chordata Node: 3975 Sequences: 301
eukaryota Node: 181514 Sequences: 803
viruses Node: 223526 Sequences: 13555
```


Public Domain notice
====================

National Center for Biotechnology Information.

This software is a "United States Government Work" under the terms of the United States
Copyright Act. It was written as part of the authors' official duties as United States
Government employees and thus cannot be copyrighted. This software is freely available
to the public for use. The National Library of Medicine and the U.S. Government have not
 placed any restriction on its use or reproduction.

Although all reasonable efforts have been taken to ensure the accuracy and reliability
of the software and data, the NLM and the U.S. Government do not and cannot warrant the
performance or results that may be obtained by using this software or data. The NLM and
the U.S. Government disclaim all warranties, express or implied, including warranties
of performance, merchantability or fitness for any particular purpose.

Please cite NCBI in any work or product based on this material.
    
