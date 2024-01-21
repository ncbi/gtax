.. _database:

#############################################
Use existing GTax database metadata in Python
#############################################

Download current Python objects in pickle format from GCP. Find latest version from: https://console.cloud.google.com/storage/browser/gtax-database/ 

.. code-block:: bash

    localhost:~> gsutil -u <your-GCP-project-ID> -m cp gs://gtax-database/<latest_version>/fasta/taxonomy.pickle .
    localhost:~> gsutil -u <your-GCP-project-ID> -m cp gs://gtax-database/<latest_version>/fasta/taxonomy_groups.pickle .

Loading data in Python

.. code-block:: python

    from gtax.taxonomy import Taxonomy
    taxonomy = Taxonomy(tax_pickle_file='taxonomy.pickle', group_pickle_file = 'taxonomy_groups.pickle')

Output:

.. code-block:: text

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

Raw files
=========

FASTA and taxonomy maps
-----------------------

.. code-block:: bash

    localhost:~> gsutil -u <your-GCP-project-ID> -m cp gs://gtax-database/<latest_version>/fasta .

BLAST databases
---------------

.. code-block:: bash

    localhost:~> gsutil -u <your-GCP-project-ID> -m cp gs://gtax-database/<latest_version>/blastdb .

Kraken2 databases
---------------

.. code-block:: bash

    localhost:~> gsutil -u <your-GCP-project-ID> -m cp gs://gtax-database/<latest_version>/kraken2 .
