import json
import os

from Bio import SeqIO


def use_sequence(accession):
    if accession.startswith('NW'):
        return False
    if accession.startswith('NZ'):
        if accession.startswith('NZ_CM') or accession.startswith('NZ_CP'):
            return True
        return False
    return True


def create_taxonomy_group_fasta(db):
    ids = {}

    if not os.path.exists('{}/ncbi_dataset/data/assembly_data_report.jsonl'.format(db)):
        raise Exception('File {}/ncbi_dataset/data/assembly_data_report.jsonl '
                        'don\'t exists'.format(db))

    print(db)
    fstream = open('{}.fsa'.format(db), 'w')
    fstream_tax = open('{}_taxid'.format(db), 'w')
    fstream_idx = open('{}.idx'.format(db), 'w')

    assemblies = {}
    with open('{}/ncbi_dataset/data/assembly_data_report.jsonl'.format(db)) as fjson:
        for line in fjson.readlines():
            d = json.loads(line)
            assemblies[d['accession']] = d['organism']['taxId']
    for s in assemblies:
        files = [f for ds, dr, files in os.walk('{}/ncbi_dataset/data/{}'.format(db, s))
                 for f in files if
                 f.endswith('.fna')]
        for f in files:
            for r in SeqIO.parse('{}/ncbi_dataset/data/{}/{}'.format(db, s, f), 'fasta'):
                seq_len = len(r.seq)
                if seq_len >= 1000 and use_sequence(r.id):
                    if not ids.setdefault(r.id, False):
                        ids[r.id] = True
                        fstream_tax.write('{}\t{}\n'.format(r.id, assemblies[s]))
                        fstream_idx.write('{}\t{}\t{}\t{}\n'.format(
                            r.id, fstream.tell(), assemblies[s], seq_len))
                        fstream.write(r.format('fasta'))
    fstream.close()
    fstream_tax.close()
    fstream_idx.close()
    print(db + ' done')


def create_taxonomy_group_eukaryotes_fasta(db, taxonomy):
    ids = {}

    if not os.path.exists('eukaryotes/ncbi_dataset/data/assembly_data_report.jsonl'):
        raise Exception('File eukaryotes/ncbi_dataset/data/assembly_data_report.jsonl'
                        ' don\'t exists')

    print(db)

    fstream = open('{}.fsa'.format(db), 'w')
    fstream_tax = open('{}_taxid'.format(db), 'w')
    fstream_idx = open('{}.idx'.format(db), 'w')

    assemblies = {}
    with open('eukaryotes/ncbi_dataset/data/assembly_data_report.jsonl') as fjson:
        for line in fjson.readlines():
            d = json.loads(line)
            if int(d['organism']['taxId']) in taxonomy.taxonomy_groups[db]['nodes']:
                assemblies[d['accession']] = d['organism']['taxId']
    for s in assemblies:
        files = [f for ds, dr, files in os.walk('eukaryotes/ncbi_dataset/data/{}'.format(s))
                 for f in files if
                 f.endswith('.fna')]
        for f in files:
            for r in SeqIO.parse('eukaryotes/ncbi_dataset/data/{}/{}'.format(s, f), 'fasta'):
                seq_len = len(r.seq)
                if seq_len >= 10000 and use_sequence(r.id):
                    if not ids.setdefault(r.id, False):
                        ids[r.id] = True
                        fstream_tax.write('{}\t{}\n'.format(r.id, assemblies[s]))
                        fstream_idx.write('{}\t{}\t{}\t{}\n'.format(
                            r.id, fstream.tell(), assemblies[s], seq_len))
                        fstream.write(r.format('fasta'))

    fstream.close()
    fstream_tax.close()
    fstream_idx.close()
    print(db + ' done')


def gtax_parallel(db, taxonomy):
    if db in ['archaea', 'bacteria', 'viruses']:
        create_taxonomy_group_fasta(db)
    else:
        create_taxonomy_group_eukaryotes_fasta(db, taxonomy)
