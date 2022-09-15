.. _blast:

#############################################
Process BLAST results to remove contamination
#############################################

After de novo transcriptome assembly, BLASTN can be used to detect contaminated transcripts
that should be removed from the assembly.

Elastic-Blast
=============

Run elastic-blast in your cloud provider as explined here_.

Use as *options* in the **ini** file:

.. code-block:: bash

    options = -task megablast -evalue 0.0001 -outfmt "6 qseqid sgi saccver length pident evalue bitscore score qcovs qcovhsp qcovus staxid"


After processing, elastic-blast will create multiple files with extension **.out.gz**

Download those file to a local folder.

Remove contamination
====================

Install GTax as described in the :ref:`Installation`.

Run this command to detect and remove contaminated transcripts.

.. code-block:: bash

        localhost:~> taxonomy_blast --threads 8 --prefix Trinity --fasta Trinity.fasta.gz --taxid 33090 --blastdir ./ --blast_columns "qseqid sgi saccver length pident evalue bitscore score qcovs qcovhsp qcovus staxid"

**--taxid** option refers to the parent taxonomy ID to use as valid taxonomies. For instance, to process
plant transcriptome, use taxid as 33090 which is the taxid of the *Viridiplantae* kingdom.

Two files will be created using the **--prefix** option, in this case **Trinity**:

 * Trinity_clean.fsa: FASTA file with decontaminated transcriptome
 * Trinity_cont.tsv: TSV file with transcript's ID and best contaminated BLAST hit



.. _here: https://blast.ncbi.nlm.nih.gov/doc/elastic-blast/
.. _GTax: