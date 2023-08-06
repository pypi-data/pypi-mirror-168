========
Overview
========

.. image:: https://badge.fury.io/py/PacbioDataProcessing.svg
	   :target: https://badge.fury.io/py/PacbioDataProcessing

.. image:: https://img.shields.io/pypi/pyversions/PacbioDataProcessing
	   :target: https://pypi.python.org/pypi/PacbioDataProcessing
	   :alt: PyPI - Python Version

.. image:: https://readthedocs.org/projects/pacbio-data-processing/badge/?version=latest
           :target: https://pacbio-data-processing.readthedocs.io/en/latest/?badge=latest
	   :alt: Documentation Status


This project is about detecting modifications of DNA in PacBio
sequencing data stored in the BAM format.
The PacBio sequencing data is processed at molecule level: each molecule/ZMW/hole number
is analyzed individually.

To learn how to start using this software, have a look at the quickstart_
section.

Or check the usage_ section, for more details.


* Free software: GNU General Public License v3
* Documentation: https://pacbio-data-processing.readthedocs.io


Features
========

* Detection of individual ``m6A`` modifications in each molecule.
* The single molecule analysis of a BAM file can be performed with a command line
  interface (CLI) program ``sm-analysis`` or using a simple graphical user interface
  (GUI) program, ``sm-analysis-gui``.
* The single molecule analysis can be parallelized to speed up the processing of
  large BAM files.
* An auxiliary executable, ``bam-filter``, is also provided.


Credits
=======

This package was created with Cookiecutter_ and the `palao/cookiecutter-genrepo-pypackage`_ project template.

.. _quickstart: https://pacbio-data-processing.readthedocs.io/en/latest/quickstart.html
.. _usage: https://pacbio-data-processing.readthedocs.io/en/latest/usage/index.html
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`palao/cookiecutter-genrepo-pypackage`: https://github.com/palao/cookiecutter-genrepo-pypackage
