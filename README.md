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
gsutil -u <you-GCP-project> -m cp -r gs://gtax-database/20221102 .
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
2464341 taxonomies loaded
bacteria Node: 537498 Sequences: 19435
archaea Node: 14266 Sequences: 798
liliopsida Node: 48464 Sequences: 317
eudicotyledons Node: 153108 Sequences: 1077
viridiplantae Node: 48003 Sequences: 185
fungi Node: 186994 Sequences: 914
arthropoda Node: 912789 Sequences: 2596
neoteleostei Node: 31205 Sequences: 1610
actinopterygii Node: 22514 Sequences: 1258
glires Node: 5490 Sequences: 2346
primates Node: 1101 Sequences: 673
carnivora Node: 783 Sequences: 437
artiodactyla Node: 1200 Sequences: 487
amphibia Node: 13009 Sequences: 122
sauropsida Node: 32051 Sequences: 1476
sarcopterygii Node: 4941 Sequences: 376
chordata Node: 4122 Sequences: 400
eukaryota Node: 194114 Sequences: 896
viruses Node: 234108 Sequences: 14233
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
    
