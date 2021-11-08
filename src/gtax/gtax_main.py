import os
from functools import partial
from multiprocessing import Pool

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
    p = Pool(len(dbs))
    results = p.map(partial(gtax_parallel, taxonomy=taxonomy), dbs)
    p.close()

    taxonomy.add_sequences_size_from_gtax_idx_all()
    taxonomy.create_pickle('taxonomy.pickle',
                           'taxonomy_groups.pickle')
