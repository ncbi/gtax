.. _installation:

############
Installation
############

************
Requirements
************

 1. NCBI Datasets (https://www.ncbi.nlm.nih.gov/datasets/docs/v1/quickstarts/command-line-tools/)

************************************
GTAX with Python virtual environment
************************************

GTAX python installation
========================

Python 3.7 or above should be installed.

.. code-block:: bash

    localhost:~> python3 -m venv gtax_venv
    localhost:~> source gtax_venv/bin/activate
    (pm4ngs_venv) localhost:~> pip install wheel
    (pm4ngs_venv) localhost:~> pip install gtax

GTAX python env activation
==========================

For activating the virtual env:

.. code-block:: bash

    localhost:~> source gtax_venv/bin/activate
    (pm4ngs_venv) localhost:~> gtax -v
    GTAX version: 0.0.1

************************
GTAX with Conda/BioConda
************************

Conda installation
==================

Conda_ should be already installed and configured using these commands:

.. code-block:: bash

    localhost:~> wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    localhost:~> sh Miniconda3-latest-Linux-x86_64.sh
    localhost:~> conda config --add channels defaults
    localhost:~> conda config --add channels bioconda
    localhost:~> conda config --add channels conda-forge	

GTAX conda installation
=======================

GTAX should be installed in a Conda virtual environment named *gtax*:

.. code-block:: bash

    localhost:~> conda create -n gtax gtax

GTAX conda env activation
===========================

For activating the conda env:

.. code-block:: bash

    localhost:~> conda activate gtax
    localhost:~> gtax -v
    GTAX version: 0.0.1

.. _Conda: https://github.com/conda/conda

