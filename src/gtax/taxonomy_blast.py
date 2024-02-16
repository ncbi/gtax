import os
import gzip
import pandas
import argparse
from Bio import SeqIO
from multiprocessing import Pool
from functools import partial
from gtax.taxonomy import Taxonomy


def transcript_contamination(filename, blast_columns, tax_ids, taxonomy):
    blast_df = pandas.read_csv(filename, sep='\t', header=None,
                               names=blast_columns.split(' '),
                               low_memory=False)
    groupby_qseqid = blast_df.groupby('qseqid')
    data = []
    for g in groupby_qseqid.groups.keys():
        df = groupby_qseqid.get_group(g)
        df = df[df['evalue'] == df['evalue'].min()]
        if not all(elem in tax_ids for elem in df['staxid'].unique()):
            df = df[~df.staxid.isin(tax_ids)].sort_values(by='bitscore', ascending=False).reset_index()
            node = taxonomy.find_node(str(df['staxid'].iloc[0]))
            if node[0]:
                node = node[0]['name_']
            else:
                node = str(df['staxid'].iloc[0])
            data.append([g, True, node, df['evalue'].iloc[0], df['sseqid'].iloc[0], df['staxid'].iloc[0]])
        else:
            data.append([g, False, False, False, False, False ])
    return data


def taxonomy_blast():
    parser = argparse.ArgumentParser(prog='taxonomy_blast',
                                     description='This tools process BLAST output to find contamination.')

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
        with Pool(processes=int(args.threads)) as p:
            results = p.map(partial(transcript_contamination,
                                    blast_columns=args.blast_columns,
                                    tax_ids=tax_ids, taxonomy=taxonomy),
                            files)
            for data in results:
                for r in data:
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
