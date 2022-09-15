import unittest

from gtax.taxonomy import Taxonomy


class TestTaxonomyMethods(unittest.TestCase):

    def test_taxonomy(self):
        self.taxonomy = Taxonomy()
        n = self.taxonomy.tax.nodes(data=True)['2']
        self.assertEqual(n['name_'], 'Bacteria')
        # self.assertEqual('Bacteria', 'Bacteria')


if __name__ == '__main__':
    unittest.main()
