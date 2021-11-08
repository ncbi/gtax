from gtax.taxonomy import Taxonomy


def taxonomy_pickle():
    taxonomy = Taxonomy()

    taxonomy.create_pickle('taxonomy.pickle',
                           'taxonomy_groups.pickle')
