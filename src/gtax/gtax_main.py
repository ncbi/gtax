import json
import os
from functools import partial
from multiprocessing import Pool
from zipfile import ZipFile

from gtax.gtax_database import gtax_parallel
from gtax.taxonomy import Taxonomy


def check_preexisting_data():
    dbs = ['archaea', 'bacteria', 'eukaryotes', 'viruses']
    for db in dbs:
        if not os.path.exists('{}/ncbi_dataset/data/assembly_data_report.jsonl'.format(db)):
            raise Exception('Folder {} does not exists. '
                            'Use datasets for downloading the data'.format(db))


def gtax_database():
    check_preexisting_data()
    taxonomy = Taxonomy()
    dbs = taxonomy.taxonomy_groups.keys()
    print('Processing {} databases'.format(dbs))
    with Pool(len(dbs)) as p:
        p.map(partial(gtax_parallel, taxonomy=taxonomy), dbs)
    taxonomy.create_taxonomy_groups()
    taxonomy.create_pickle('taxonomy.pickle',
                           'taxonomy_groups.pickle')


def filter_metadata_zip():
    superkingdoms = ['archaea', 'bacteria', 'viruses', 'eukaryotes']

    for db in superkingdoms:
        if os.path.exists('{}_meta.zip'.format(db)):
            if not os.path.exists('{}/ncbi_dataset/data'.format(db)):
                os.makedirs('{}/ncbi_dataset/data'.format(db))
            with ZipFile('{}_meta.zip'.format(db), 'r') as zip:
                assemblies = set()
                assemblies_tmp = {}
                with zip.open('ncbi_dataset/data/assembly_data_report.jsonl') as fjson, open(
                        '{}/ncbi_dataset/data/assembly_data_report.jsonl'.format(db), 'w') as fjson_out:
                    for line in fjson.readlines():
                        d = json.loads(line.decode("utf-8"))
                        v = assemblies_tmp.setdefault(d['organism']['taxId'], [])
                        v.append(d)
                    for s in assemblies_tmp.keys():
                        rep_genome = []
                        for e in assemblies_tmp[s]:
                            if 'refseqCategory' in e['assemblyInfo']:
                                rep_genome.append(e)
                        if len(rep_genome) == 1:
                            assemblies.add(rep_genome[0]['accession'])
                            fjson_out.write('{}\n'.format(json.dumps(rep_genome[0])))
                        else:
                            assemblies.add(assemblies_tmp[s][0]['accession'])
                            fjson_out.write('{}\n'.format(json.dumps(assemblies_tmp[s][0])))

                print('There are {} assemblies included'.format(len(assemblies)))
                with zip.open('ncbi_dataset/data/dataset_catalog.json') as fjson, open(
                        '{}/ncbi_dataset/data/dataset_catalog.json'.format(db), 'w') as fjson_out:
                    d = json.loads(fjson.read().decode("utf-8"))
                    catalog = []
                    for c in d['assemblies']:
                        if 'accession' in c:
                            if c['accession'] in assemblies:
                                catalog.append(c)
                        else:
                            catalog.append(c)
                    d['assemblies'] = catalog
                    fjson_out.write(json.dumps(d, indent=2))
                with zip.open('ncbi_dataset/fetch.txt') as fin, open('{}/ncbi_dataset/fetch.txt'.format(db),
                                                                     'w') as fout:
                    for line in fin.readlines():
                        line = line.decode("utf-8")
                        f = os.path.dirname(line.split('\t')[2].replace('data/', ''))
                        if f in assemblies:
                            fout.write(line)


def gtax():
    import argparse
    from argparse import RawTextHelpFormatter
    from gtax import __version__

    epilog = '''
        For more information see https://gtax.readthedocs.io/en/latest/index.html
        
        Available programs:
        
        
        filter_metadata_zip: Read the zipped metadata file for each superkingdom and create the folders 
                             for hydration with the datasets command. 
        gtax_database: Creates the FASTA, indexes and TaxID maps for the databases.
        taxonomy_blast: Process BLAST output to find contamination.
        
        Cite: 
        
        Alvarez, R.V., Landsman, D. GTax: improving de novo transcriptome assembly by removing foreign RNA 
        contamination. Genome Biol 25, 12 (2024). https://doi.org/10.1186/s13059-023-03141-2
    '''
    parser = argparse.ArgumentParser(prog='gtax',
                                     description='GTax python package provides tools for the creation '
                                                 'of the GTax sequence-based database.',
                                     epilog=epilog,
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()
    parser.print_help()
