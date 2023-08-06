.. highlight:: shell

.. _bam-filter:

Filtering Bam files with ``bam-filter``
=======================================

This executable is useful to filter :ref:`aligned-PacBio-bam-file`'s
according to the values of some columns. It offers the following
options:

.. program:: bam-filter

.. option:: <BAM-FILE>

   Input file in BAM format. The output will be another
   BAM-FILE with the same name but prefixed with 'parsed.'.

   For example:

   .. code-block:: console

    $ bam-filter mydata.bam ...

   will produce, as output a file named ``parsed.mydata.bam``.

.. option:: -l <INT>, --min-dna-seq-length <INT>

   Minimum length of DNA sequence to be kept (default: 0, ie. do not
   filter).

.. option:: -r <INT>, --min-subreads-per-molecule <INT>

   Minimum number of subreads per molecule to keep it (default: 1).

.. option:: -q <INT>, --quality-threshold <INT>

   Quality threshold of the sample. Between 0 (the lowest) and 255
   (the highest) (default: 0).

.. option:: -m <MAPPING>[ <MAPPING> ...], --mappings <MAPPING>[ <MAPPING> ...]

   Keep only the requested (space separated) list of mappings
   (default: keep all).

.. option:: -R <NUM>, --min-relative-mapping-ratio <NUM>

   Minimum ratio (wanted mappings/all mappings) to keep the subread
   (by default all the subreads are taken).
