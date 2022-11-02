.. _datasets:

####################
Create GTax database
####################

Download genomes data with NCBI Datsets
---------------------------------------

GTax uses four taxonomy superkingdoms for downloading data: *archaea*, *bacteria*, *viruses* and *eukaryotes*

Users need to run these commands to download the genomes sequences:

Datasets
========

.. code-block:: bash

    localhost:~> wget https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets
    localhost:~> chmod a+x datasets

Archaea
=======

.. code-block:: bash

    localhost:~> ./datasets download genome taxon 2157 --assembly-source refseq --dehydrated --filename archaea_meta.zip

Bacteria
========

.. code-block:: bash

    localhost:~> ./datasets download genome taxon 2 --assembly-source refseq --dehydrated --filename bacteria_meta.zip

Viruses
=======

.. code-block:: bash

    localhost:~> ./datasets download genome taxon 10239 --assembly-source refseq --dehydrated --filename viruses_meta.zip

Eukaryotes
==========

.. code-block:: bash

    localhost:~> ./datasets download genome taxon 2759 --assembly-source refseq --dehydrated --filename eukaryotes_meta.zip

Process metadata and creates the directories for hydration
----------------------------------------------------------

The command **filter_metadata_zip** will read the zipped metadata file for each superkingdom and create the folders for
hydration with the **datasets** command. This command will keep the reference genome for each taxa if it is available.
If no reference genome is available, the latest assembly will be kept.

.. code-block:: bash

    localhost:~> filter_metadata_zip

Hydrate directories with datasets
---------------------------------

Archaea
=======

.. code-block:: bash

    localhost:~> ./datasets rehydrate --directory archaea/

Bacteria
========

.. code-block:: bash

    localhost:~> ./datasets rehydrate --directory bacteria/

Viruses
=======

.. code-block:: bash

    localhost:~> ./datasets rehydrate --directory viruses/

Eukaryotes
==========

.. code-block:: bash

    localhost:~> ./datasets rehydrate --directory eukaryotes/

Create Gtax FASTA files
-----------------------

After all data is downloaded, it will take few hours to finish, we can create the FASTA, indexes and TaxID maps for the
databases.

.. code-block:: bash

    localhost:~> gtax_database

