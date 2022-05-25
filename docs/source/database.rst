.. _database:

#############################################
Use existing GTax database metadata in Python
#############################################

Download current Python objects in pickle format from GCP

.. code-block:: bash

    localhost:~> gsutil -u <your-GCP-project-ID> -m cp gs://gtax-database/20211025/fasta/taxonomy.pickle .
    localhost:~> gsutil -u <your-GCP-project-ID> -m cp gs://gtax-database/20211025/fasta/taxonomy_groups.pickle .

Loading data in Python

.. code-block:: python

    from gtax.taxonomy import Taxonomy
    taxonomy = Taxonomy(tax_pickle_file='taxonomy.pickle', group_pickle_file = 'taxonomy_groups.pickle')

Output:

.. code-block:: text

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
