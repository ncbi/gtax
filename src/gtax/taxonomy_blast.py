import os
import gzip
import pandas
import argparse
from Bio import SeqIO
from multiprocessing import Pool
from functools import partial
from gtax.taxonomy import Taxonomy


def transcript_contamination(t, blast_df, tax_ids, taxonomy):
    df = blast_df[blast_df['qseqid'] == t].copy()
    if not df.empty:
        df = df[df['evalue'] == df['evalue'].min()]
        if not all(elem in tax_ids for elem in df['staxid'].unique()):
            df = df[~df.staxid.isin(tax_ids)].sort_values(by='bitscore', ascending=False).reset_index()
            node = taxonomy.find_node(str(df['staxid'].iloc[0]))
            if node[0]:
                node = node[0]['name_']
            else:
                node = str(df['staxid'].iloc[0])
            return t, True, node, df['evalue'].iloc[0], df['saccver'].iloc[0], df['staxid'].iloc[0]
    return t, False


def taxonomy_blast():
    parser = argparse.ArgumentParser()

    parser.add_argument('--threads', help='No. of threads',
                        required=True)
    parser.add_argument('--prefix', help='Prefix for output files',
                        required=True)
    parser.add_argument('--fasta', help='Reference Transcriptome FASTA file',
                        required=True)
    parser.add_argument('--taxid', help='Parent TaxID to use as filter',
                        required=True)
    parser.add_argument('--blastdir', help='Directory with BLAST gzip results *.out.gz',
                        required=True)
    parser.add_argument('--blast_columns', help='BLAST -outfmt columns. Must include '
                                                'qseqid, saccver, evalue, qcovs, staxid',
                        required=True)
    args = parser.parse_args()

    taxonomy = Taxonomy()

    tax_ids = [int(i) for i in taxonomy.successors(args.taxid)]
    print('{} taxonomies IDs in the list'.format(len(tax_ids)))

    records = {}
    with gzip.open(args.fasta, 'rt') as handle:
        for record in SeqIO.parse(handle, "fasta"):
            records[record.id] = record
    print(f"{len(records)} sequences loaded")

    files = [os.path.join(args.blastdir, f)
             for f in os.listdir(args.blastdir) if f.endswith('.out.gz')]

    contamination = 0
    cont_ids = set()
    with open('{}_cont.tsv'.format(args.prefix), 'w') as f_cont:
        f_cont.write('transcript\tsubject\tevalue\ttax_id\ttaxa\n')
        for f in files:
            blast_df = pandas.read_csv(f, sep='\t', header=None,
                                           names=args.blast_columns.split(' '),
                                           low_memory=False)
            print(f"{len(blast_df)} BLAST results loaded from {f}")
            with Pool(processes=int(args.threads)) as p:
                results = p.map(partial(transcript_contamination,
                                        blast_df=blast_df,
                                        tax_ids=tax_ids, taxonomy=taxonomy),
                                blast_df.qseqid.unique())
                for r in results:
                    if r[1]:
                        contamination += 1
                        cont_ids.add(r[0])
                        f_cont.write('{}\t{}\t{}\t{}\t{}\n'.format(r[0], r[4], r[3], r[5], r[2]))
    with open('{}_clean.fsa'.format(args.prefix), 'w') as f_fsa:
        for r in records:
            if r not in cont_ids:
                f_fsa.write(records[r].format('fasta'))
    print(f'Input Transcripts: {len(records)}\n'
          f'Clean Transcripts: {len(records) - contamination}\n'
          f'Contaminated transcripts: {contamination}')
