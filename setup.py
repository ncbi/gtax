import os
import os.path

from setuptools import find_packages
from setuptools import setup


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        return f.read()

# Set __version__
exec(open('src/gtax/__init__.py').read())

setup(
    name='gtax',
    packages=find_packages(where='src'),
    package_dir={
        '': 'src',
    },
    data_files=[('', ['README.md'])],
    use_scm_version=True,
    setup_requires=['wheel', 'setuptools_scm'],
    description='Gtax generate a taxonomy sequence database by genomes ',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='Public Domain',
    author='Vera Alvarez, Roberto',
    author_email='veraalva' '@' 'ncbi.nlm.nih.gov',
    maintainer='Vera Alvarez, Roberto',
    maintainer_email='veraalva' '@' 'ncbi.nlm.nih.gov',
    url='https://github.com/ncbi/gtax',
    install_requires=['biopython',
                      'networkx',
                      'numpy',
                      'pandas',
                      'requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    keywords='Biocontainers',
    project_urls={
        'Documentation': 'https://gtax.readthedocs.io/',
        'Source': 'https://github.com/ncbi/gtax',
        'Tracker': 'https://github.com/ncbi/gtax/issues',
    },
    entry_points={
        'console_scripts': [
            'gtax = gtax.gtax_main:gtax',
            'taxonomy_pickle = gtax.taxonomy_main:taxonomy_pickle',
            'gtax_database = gtax.gtax_main:gtax_database',
            'filter_metadata_zip = gtax.gtax_main:filter_metadata_zip',
            'create_random_short_sequences = gtax.sequence:create_random_short_sequences',
            'sequence_binning = gtax.sequence_binning:sequence_binning_main',
            'taxonomy_blast = gtax.taxonomy_blast:taxonomy_blast'
        ],
    }
)
